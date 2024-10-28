from sys import getsizeof
from pool import Pool
import json

# pool = Pool()
# pool.getPoolStatus();

data = {"model": {"class_name": "Sequential", "config": {"name": "sequential", "layers": [{"class_name": "InputLayer", "config": {"batch_input_shape": ["null", 3], "dtype": "float32", "sparse": "false", "ragged": "false", "name": "dense_input"}}, {"class_name": "Dense", "config": {"name": "dense", "trainable": "true", "batch_input_shape": ["null", 3], "dtype": "float32", "units": 32, "activation": "relu", "use_bias": "true", "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": "null"}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": "null", "bias_regularizer": "null", "activity_regularizer": "null", "kernel_constraint": "null", "bias_constraint": "null"}}, {"class_name": "Dense", "config": {"name": "dense_1", "trainable": "true", "dtype": "float32", "units": 1, "activation": "sigmoid", "use_bias": "true", "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": "null"}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": "null", "bias_regularizer": "null", "activity_regularizer": "null", "kernel_constraint": "null", "bias_constraint": "null"}}]}, "keras_version": "2.8.0", "backend": "tensorflow"}, "cardinality": "1"}
data = json.dumps(data)
jsonData = {
                'index': 1,
                'timestamp': "text",
                'proof': 1,
                'typeBlock': "result",
                'previousHash': hash(data),
                'hostTrainer': "h3",
                'transactions': data
            }
data2 = json.dumps(jsonData)
print(f'tamanho do modelo : {getsizeof(data2)} bytes')