from model import load_model

model = load_model("./model_save/model")

# data - np.array(obj1, obj2, ...)
def predict(data):
    predict = model.predict(data)
    return predict