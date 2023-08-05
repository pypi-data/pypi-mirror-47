#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module is for performing bayesian optimization on algorithms
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import importlib

from hyperopt import hp, fmin, tpe, Trials, STATUS_OK, space_eval
import pandas as pd

# import sys
# sys.path.append("../")
# from config.global_config import KnowledgeGraph
from pykg2vec.config.global_config import KnowledgeGraph
# from utils.trainer import Trainer
from pykg2vec.utils.trainer import Trainer
from pprint import pprint

# model_path = "core"
model_path = "pykg2vec.core"
# config_path = "config.config"
config_path = "pykg2vec.config.config"
# hyper_param_path = "config.hyperparams"
hyper_param_path = "pykg2vec.config.hyperparams"

modelMap = {"complex": "Complex",
            "conve": "ConvE",
            "distmult": "DistMult",
            "distmult2": "DistMult2",
            "kg2e": "KG2E",
            "ntn": "NTN",
            "proje_pointwise": "ProjE_pointwise",
            "rescal": "Rescal",
            "rotate": "RotatE",
            "slm": "SLM",
            "sme": "SME",
            "transd": "TransD",
            "transe": "TransE",
            "transh": "TransH",
            "transm": "TransM",
            "transR": "TransR",
            "tucker": "TuckER",
            "tucker_v2": "TuckER_v2"}


configMap = {"complex": "ComplexConfig",
             "conve": "ConvEConfig",
             "distmult": "DistMultConfig",
             "distmult2": "DistMultConfig",
             "kg2e": "KG2EConfig",
             "ntn": "NTNConfig",
             "proje_pointwise": "ProjE_pointwiseConfig",
             "rescal": "RescalConfig",
             "rotate": "RotatEConfig",
             "slm": "SLMConfig",
             "sme": "SMEConfig",
             "transd": "TransDConfig",
             "transe": "TransEConfig",
             "transh": "TransHConfig",
             "transm": "TransMConfig",
             "transR": "TransRConfig",
             "tucker": "TuckERConfig",
             "tucker_v2": "TuckERConfig"}


hypMap = {"complex": "ComplexParams",
          "conve": "ConvEParams",
          "distmult": "DistMultParams",
          "distmult2": "DistMultParams",
          "kg2e": "KG2EParams",
          "ntn": "NTNParams",
          "proje_pointwise": "ProjE_pointwiseParams",
          "rescal": "RescalParams",
          "rotate": "RotatEParams",
          "slm": "SLMParams",
          "sme": "SMEParams",
          "transd": "TransDParams",
          "transe": "TransEParams",
          "transh": "TransHParams",
          "transm": "TransMParams",
          "transR": "TransRParams",
          "tucker": "TuckERParams",
          "tucker_v2": "TuckERParams"}


class BaysOptimizer(object):

    def __init__(self, name_dataset='Freebase15k', sampling="uniform", args=None):
        """store the information of database"""
        model_name = args.model.lower()
        self.args = args
        self.knowledge_graph = KnowledgeGraph(dataset=name_dataset, negative_sample=sampling)
        hyper_params = None
        try:
            self.model_obj = getattr(importlib.import_module(model_path + ".%s" % modelMap[model_name]),
                                     modelMap[model_name])
            self.config_obj = getattr(importlib.import_module(config_path), configMap[model_name])
            hyper_params = getattr(importlib.import_module(hyper_param_path), hypMap[model_name])()

        except ModuleNotFoundError:
            print("%s not implemented! Select from: %s" % (model_name,
                                                           ' '.join(map(str, modelMap.values()))))
        config = self.config_obj()
        config.data=name_dataset
        # config.set_dataset(name_dataset)
        self.trainer = Trainer(model=self.model_obj(config), debug=self.args.debug, tuning=True)
        self.search_space = self.define_search_space(hyper_params)
        
    def define_search_space(self, hyper_params):
        space = {k: hp.choice(k, v) for k, v in hyper_params.__dict__.items() if not k.startswith('__') and not callable(k)}
        return space

    def optimize(self):
        space = self.search_space
        trials = Trials()
        
        best_result = fmin(fn=self.get_loss, space=space, algo=tpe.suggest, max_evals=2, trials=trials)
        
        columns = list(space.keys())   
        results = pd.DataFrame(columns=['iteration'] + columns + ['loss'])
        
        for idx, trial in enumerate(trials.trials):
            row = []
            row.append(idx)
            translated_eval = space_eval(self.search_space, {k: v[0] for k, v in trial['misc']['vals'].items()})
            for k in columns:
                row.append(translated_eval[k])
            row.append(trial['result']['loss'])
            results.loc[idx] = row

        path = self.trainer.config.result / self.trainer.model.model_name 
        path.mkdir(parents=True, exist_ok=True)
        results.to_csv(str(path / "trials.csv"), index=False)
        
        print(results)
        print('Found Golden Setting:')
        pprint(space_eval(space, best_result))

    def get_loss(self, params):
        self.trainer.config.L1_flag = params['L1_flag']
        self.trainer.config.batch_size = params['batch_size']
        self.trainer.config.epochs = params['epochs']
        self.trainer.config.hidden_size = params['hidden_size']
        self.trainer.config.learning_rate = params['learning_rate']
        self.trainer.config.margin = params['margin']
        self.trainer.config.disp_result = False
        self.trainer.config.disp_summary = False
        self.trainer.config.save_model = False
        self.trainer.config.debug = True
        self.trainer.config.test_num = 1000

        self.trainer.build_model()
        self.trainer.summary_hyperparameter()
    
        loss = self.trainer.tune_model()
        # loss = self.trainer.train_model(tuning=True)

        return {'loss': loss, 'status': STATUS_OK}