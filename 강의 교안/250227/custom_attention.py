import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense, Concatenate, Activation

class CustomAttention(Layer):
    def __init__(self, units=64, score_type='luong', **kwargs):
        super(CustomAttention, self).__init__(**kwargs)
        self.units = units
        self.score_type = score_type
        
    def build(self, input_shape):
        # Luong style
        self.luong_wa = Dense(input_shape[-1], use_bias=False)
        
        # Bahdanau style
        self.bahdanau_w1 = Dense(self.units, use_bias=False)
        self.bahdanau_w2 = Dense(self.units, use_bias=False)
        self.bahdanau_v = Dense(1, use_bias=False)
        
        # Output transformation
        self.w_c = Dense(self.units, use_bias=False, activation='tanh')
        
        # Other layers
        self.concat = Concatenate()
        super(CustomAttention, self).build(input_shape)
        
    def call(self, inputs, **kwargs):
        # Get last hidden state
        h_t = inputs[:, -1:, :]  # (batch_size, 1, units)
        h_s = inputs[:, :-1, :]  # (batch_size, time-1, units)
        
        # Calculate attention scores
        if self.score_type == 'luong':
            # Luong's multiplicative style
            score = tf.matmul(h_t, self.luong_wa(h_s), transpose_b=True)
        else:
            # Bahdanau's additive style
            h_t_expanded = tf.tile(h_t, [1, tf.shape(h_s)[1], 1])
            score = self.bahdanau_v(
                tf.tanh(self.bahdanau_w1(h_t_expanded) + self.bahdanau_w2(h_s))
            )
        
        # Calculate attention weights
        attention_weights = tf.nn.softmax(score, axis=-1)
        
        # Apply attention weights
        context = tf.matmul(attention_weights, h_s)
        
        # Combine context with last hidden state
        h_t = tf.squeeze(h_t, axis=1)
        context = tf.squeeze(context, axis=1)
        attention_output = self.w_c(self.concat([context, h_t]))
        
        return attention_output
        
    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.units)
        
    def get_config(self):
        config = super(CustomAttention, self).get_config()
        config.update({
            'units': self.units,
            'score_type': self.score_type
        })
        return config 