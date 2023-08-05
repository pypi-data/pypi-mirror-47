#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

# import sys
# sys.path.append("../")
# from core.KGMeta import ModelMeta
from pykg2vec.core.KGMeta import ModelMeta


class TuckER(ModelMeta):
    """
    ------------------Paper Title-----------------------------
    TuckER: Tensor Factorization for Knowledge Graph Completion
    ------------------Paper Authors---------------------------
    Ivana Balazevi ˇ c´1 Carl Allen 1 Timothy M. Hospedales 1
    1School of Informatics, University of Edinburgh,
    United Kingdom. Correspondence to: Ivana Balazevi ˇ c´
    <ivana.balazevic@ed.ac.uk>.
    ------------------Summary---------------------------------
    TuckER is a Tensor-factorization-based embedding technique based on
    the Tucker decomposition of a third-order binary tensor of triplets. Although
    being fully expressive, the number of parameters used in Tucker only grows linearly
    with respect to embedding dimension as the number of entities or relations in a
    knowledge graph increases.
    """

    def __init__(self, config=None):
        self.config = config
        self.data_stats = self.config.kg_meta
        self.model_name = 'TuckER'
        
        self.def_layer()

    def def_inputs(self):
        self.h = tf.placeholder(tf.int32, [None])
        self.r = tf.placeholder(tf.int32, [None])
        self.t = tf.placeholder(tf.int32, [None])
        self.hr_t = tf.placeholder(tf.float32, [None, self.data_stats.tot_entity])
        self.rt_h = tf.placeholder(tf.float32, [None, self.data_stats.tot_entity])

        self.test_h_batch = tf.placeholder(tf.int32, [None])
        self.test_t_batch = tf.placeholder(tf.int32, [None])
        self.test_r_batch = tf.placeholder(tf.int32, [None])

    def def_parameters(self):
        num_total_ent = self.data_stats.tot_entity
        num_total_rel = self.data_stats.tot_relation
        self.d1 = self.config.ent_hidden_size
        self.d2 = self.config.rel_hidden_size

        with tf.name_scope("embedding"):
            self.E = tf.get_variable(name="ent_embedding", shape=[num_total_ent, self.d1],
                                     initializer=tf.contrib.layers.xavier_initializer(uniform=False))
            self.R = tf.get_variable(name="rel_embedding", shape=[num_total_rel, self.d2],
                                     initializer=tf.contrib.layers.xavier_initializer(uniform=False))
        with tf.name_scope("W"):
            self.W = tf.get_variable(name="W", shape=[self.d2, self.d1, self.d1],
                                     initializer=tf.initializers.random_uniform(minval=-1, maxval=1))
        self.parameter_list = [self.E, self.R, self.W]

    def def_layer(self):
        self.inp_drop = tf.keras.layers.Dropout(rate=self.config.input_dropout)
        self.hidden_dropout1 = tf.keras.layers.Dropout(rate=self.config.hidden_dropout1)
        self.hidden_dropout2 = tf.keras.layers.Dropout(rate=self.config.hidden_dropout2)

        self.bn0 = tf.keras.layers.BatchNormalization(trainable=True)
        self.bn1 = tf.keras.layers.BatchNormalization(trainable=True)

    def forward(self, e1, r):
        norm_E = tf.nn.l2_normalize(self.E, axis=1)
        norm_R = tf.nn.l2_normalize(self.R, axis=1)

        e1 = tf.nn.embedding_lookup(norm_E, e1)
        rel = tf.squeeze(tf.nn.embedding_lookup(norm_R, r))

        e1 = self.bn0(e1)
        e1 = self.inp_drop(e1)
        e1 = tf.reshape(e1, [-1, 1, self.config.ent_hidden_size])

        W_mat = tf.matmul(rel, tf.reshape(self.W, [self.d2, -1]))
        W_mat = tf.reshape(W_mat, [-1, self.d1, self.d1])
        W_mat = self.hidden_dropout1(W_mat)

        x = tf.matmul(e1, W_mat)
        x = tf.reshape(x, [-1, self.d1])
        x = self.bn1(x)
        x = self.hidden_dropout2(x)
        x = tf.matmul(x, tf.transpose(norm_E))
        return tf.nn.sigmoid(x)

    def def_loss(self):
        pred_tails = self.forward(self.h, self.r)
        pred_heads = self.forward(self.t, self.r)

        hr_t = self.hr_t * (1.0 - self.config.label_smoothing) + 1.0 / self.data_stats.tot_entity
        rt_h = self.rt_h * (1.0 - self.config.label_smoothing) + 1.0 / self.data_stats.tot_entity

        loss_tails = tf.reduce_mean(tf.keras.backend.binary_crossentropy(hr_t, pred_tails))
        loss_heads = tf.reduce_mean(tf.keras.backend.binary_crossentropy(rt_h, pred_heads))

        reg_losses = tf.nn.l2_loss(self.E) + tf.nn.l2_loss(self.R) + tf.nn.l2_loss(self.W)

        self.loss = loss_heads + loss_tails + self.config.lmbda * reg_losses

    def test_batch(self):
        pred_tails = self.forward(self.test_h_batch, self.test_r_batch)
        pred_heads = self.forward(self.test_t_batch, self.test_r_batch)

        _, head_rank = tf.nn.top_k(pred_tails, k=self.data_stats.tot_entity)
        _, tail_rank = tf.nn.top_k(pred_heads, k=self.data_stats.tot_entity)

        return head_rank, tail_rank

    def embed(self, h, r, t):
        """function to get the embedding value"""
        emb_h = tf.nn.embedding_lookup(self.E, h)
        emb_r = tf.nn.embedding_lookup(self.R, r)
        emb_t = tf.nn.embedding_lookup(self.E, t)
        return emb_h, emb_r, emb_t

    def get_embed(self, h, r, t, sess=None):
        """function to get the embedding value in numpy"""
        emb_h, emb_r, emb_t = self.embed(h, r, t)
        h, r, t = sess.run([emb_h, emb_r, emb_t])
        return h, r, t

    def get_proj_embed(self, h, r, t, sess):
        """function to get the projected embedding value in numpy"""
        return self.get_embed(h, r, t, sess)
