#
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#

import tensorflow as tf

import kglib.kgcn.core.ingest.traverse.data.context.neighbour as neighbour
from kglib.kgcn.core.ingest.encode import tf_hub, boolean, schema
from kglib.kgcn.core.ingest.traverse.schema import traversal as trav, executor as schema_ex

GET_THING_TYPES_QUERY = "match $x sub thing; get;"
GET_ROLE_TYPES_QUERY = "match $x sub role; get;"
NO_DATA_TYPE = ''  # TODO Pass this to traversal/executor


def encode_all(context_arrays, encoders, name='encode_all'):
    """
    Take data from traversals and build neighbourhood_depths
    :param encoders: encoder to use for each key in the supplied dictionaries
    :param context_arrays: expects a list of dictionaries, one for each depth, each key referring to an array of the raw
    features of the traversals
    :param name: name for operation graph
    :return:
    """

    with tf.name_scope(name) as scope:
        encoded_arrays = []
        for context_array in context_arrays:
            all_encoded_features = []
            for key, features_array in context_array.items():
                encoded_features = encoders[key](features_array)
                all_encoded_features.append(encoded_features)
                tf.summary.histogram(key, encoded_features)

            concatenated_encoded_features = tf.concat(all_encoded_features, -1)
            tf.summary.histogram('concat', concatenated_encoded_features)
            encoded_arrays.append(concatenated_encoded_features)

        return encoded_arrays


class Encoder:
    def __init__(self, schema_tx):
        ################################################################################################################
        # Schema Traversals
        ################################################################################################################

        # This depends upon the schema being the same for the keyspace used in training vs eval and predict
        schema_traversal_executor = schema_ex.TraversalExecutor(schema_tx)

        # THINGS
        thing_schema_traversal = trav.traverse_schema(schema_traversal_executor, GET_THING_TYPES_QUERY)

        # ROLES
        role_schema_traversal = trav.traverse_schema(schema_traversal_executor, GET_ROLE_TYPES_QUERY)
        role_schema_traversal['has'] = ['has']

        ############################################################################################################
        # Encoders Initialisation
        ############################################################################################################

        with tf.name_scope('encoding_init') as scope:
            thing_encoder = schema.MultiHotSchemaTypeEncoder(thing_schema_traversal, name='thing_encoder')
            role_encoder = schema.MultiHotSchemaTypeEncoder(role_schema_traversal, name='role_encoder')

            # In case of issues https://github.com/tensorflow/hub/issues/61
            string_encoder = tf_hub.TensorFlowHubEncoder(
                "https://tfhub.dev/google/nnlm-en-dim128-with-normalization/1", 128)

            data_types = list(neighbour.DATA_TYPE_NAMES)
            data_types.insert(0, NO_DATA_TYPE)  # For the case where an entity or relation is encountered
            data_types_traversal = {data_type: data_types for data_type in data_types}

            # Later a hierarchy could be added to data_type meaning. e.g. long and double are both numeric
            data_type_encoder = schema.MultiHotSchemaTypeEncoder(data_types_traversal, name='data_type_encoder')

        self._encoders = {
            'role_type': role_encoder,
            'role_direction': lambda x: tf.to_float(x, 'role_dir_to_float'),
            'neighbour_type': thing_encoder,
            'neighbour_data_type': lambda x: data_type_encoder(tf.convert_to_tensor(x)),
            'neighbour_value_long': lambda x: tf.to_float(x, name='long_to_float'),
            'neighbour_value_double': lambda x: x,
            'neighbour_value_boolean': lambda x: tf.to_float(
                boolean.one_hot_boolean_encode(x, 'boolean_1_hot'), name='boolean_to_float'),
            'neighbour_value_date': lambda x: tf.nn.l2_normalize(tf.to_float(x, name='date_to_float')),
            'neighbour_value_string': string_encoder
        }

    def __call__(self, shuffled_batch_arrays):
        encoded_arrays = encode_all(shuffled_batch_arrays, self._encoders)
        print('Encoded shapes')
        print([encoded_array.shape for encoded_array in encoded_arrays])
        return encoded_arrays
