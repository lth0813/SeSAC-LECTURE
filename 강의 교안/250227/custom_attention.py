import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense, Concatenate, Activation, Dot, RepeatVector, Add

class CustomAttention(Layer):
    def __init__(self, units=128, score_type='luong', **kwargs):
        super(CustomAttention, self).__init__(**kwargs)
        self.units = units
        self.score_type = score_type
        
    def build(self, input_shape):
        # Luong style
        input_dim = input_shape[-1]
        self.luong_w = Dense(input_dim, use_bias=False, name='luong_w')
        self.luong_dot = Dot(axes=[2, 2], name='luong_dot')
        
        # Bahdanau style
        self.bahdanau_w1 = Dense(input_dim, use_bias=False, name='bahdanau_w1')
        self.bahdanau_w2 = Dense(input_dim, use_bias=False, name='bahdanau_w2')
        self.bahdanau_v = Dense(1, use_bias=False, name='bahdanau_v')
        self.bahdanau_tanh = Activation('tanh', name='bahdanau_tanh')
        self.bahdanau_add = Add(name='bahdanau_add')
        
        # Attention weight softmax
        self.softmax_normalizer = Activation('softmax', name='attention_weights')

        # Dot product for context vector
        self.dot_context = Dot(axes=[2, 1], name='context_vector')

        # Final transformation
        self.concat = Concatenate(name='concat_c_h')
        self.w_c = Dense(self.units, use_bias=False, activation='tanh', name='attention_vector')

        super(CustomAttention, self).build(input_shape)
        
    def call(self, inputs, **kwargs):
        # Get last hidden state
        h_s = inputs  # (batch_size, time_steps, units)
        h_t = h_s[:, -1:, :]  # (batch_size, 1, units)
        
        # Calculate attention scores
        if self.score_type == 'luong':
            score = self.luong_dot([h_t, self.luong_w(h_s)])
        else:
            a1 = self.bahdanau_w1(h_t)
            a2 = self.bahdanau_w2(h_s)
            a1 = RepeatVector(tf.shape(h_s)[1])(a1)
            score = self.bahdanau_tanh(self.bahdanau_add([a1, a2]))
            score = self.bahdanau_v(score)
            score = tf.squeeze(score, axis=-1)
        
        # Compute attention weights
        attention_weights = self.softmax_normalizer(score)  # (batch_size, time_steps)
        attention_weights = tf.expand_dims(attention_weights, axis=1)  # (batch_size, 1, time_steps)

        # Compute context vector
        context = self.dot_context([attention_weights, h_s])  # (batch_size, 1, units)

        # Combine context with last hidden state
        h_t = tf.squeeze(h_t, axis=1)  # (batch_size, units)
        context = tf.squeeze(context, axis=1)  # (batch_size, units)
        attention_output = self.w_c(self.concat([context, h_t]))  # (batch_size, units)

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