try:
    import tensorflow as tf
    TENSORFLOW_INSTALLED = True
    #Logger.log("Tensorflow imported")
except:
    TENSORFLOW_INSTALLED = False
    #Logger.log("Error importing Tensorflow")


class ImageClassifier():
    def __init__(self):
        return

    def load_graph(self, model_file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)

        return graph

    def read_tensor_from_image_file(self, file_name, input_height=299, input_width=299,
                                    input_mean=0, input_std=255):
        input_name = "file_reader"
        output_name = "normalized"
        file_reader = tf.read_file(file_name, input_name)
        if file_name.endswith(".png"):
            image_reader = tf.image.decode_png(file_reader, channels=3, name='png_reader')
        elif file_name.endswith(".gif"):
            image_reader = tf.squeeze(tf.image.decode_gif(file_reader, name='gif_reader'))
        elif file_name.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
        else:
            image_reader = tf.image.decode_jpeg(file_reader, channels=3, name='jpeg_reader')
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        sess = tf.Session()
        result = sess.run(normalized)

        return result

    def load_labels(self, label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label

    def get_graph_sizes(self):
        data = [
            {'text': "0.25 (Sehr schnell)", 'value': '0.25'},
            {'text': "0.50 (Schnell)", 'value': '0.50'},
            {'text': "0.75 (Normal)", 'value': '0.75'},
            {'text': "1.0 (Langsam)", 'value': '1.0'}
        ]

        return data

    def get_image_sizes(self):
        data = [
            {'text': "128 (Sehr schnell)", 'value': '128'},
            {'text': "160 (Schnell)", 'value': '160'},
            {'text': "192 (Normal)", 'value': '192'},
            {'text': "224 (Langsam)", 'value': '224'}
        ]
        return data