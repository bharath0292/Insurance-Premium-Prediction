class Predict:
    def __init__(self,model,data):

        self.model = model
        self.data = data


    def predict(self):
        return self.model.predict(self.data)