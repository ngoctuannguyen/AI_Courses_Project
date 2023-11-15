import nn
import os

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)
        self.batch_size = 1

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w, x) # nhân vô hướng 2 vector 


    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"

        # if nn.as_scalar(self.run(x)) >= 0:
        #     return 1
        # else: 
        #     return -1
        distance = nn.as_scalar(self.run(x))
        return 1 if distance >= 0 else -1 # dùng toán tử 3 ngồi để flex :D

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        mistake = True # đặt flag
        while mistake:
            mistake = False
            for x, y in dataset.iterate_once(self.batch_size):
                pred = self.get_prediction(x) # dự đoán từ model
                if pred != nn.as_scalar(y): # nếu chưa đúng thì train tiếp 
                    mistake = True
                    self.w.update(x, nn.as_scalar(y)) # update thông qua gradient descent
 
class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 200
        self.learning_rate = 0.05
        self.hidden_layer = 512
        self.first_weights = nn.Parameter(1, self.batch_size)
        self.fb = nn.Parameter(1, self.batch_size)
        self.second_weights = nn.Parameter(self.batch_size, self.hidden_layer)
        self.sb = nn.Parameter(1, self.hidden_layer)
        self.third_weights = nn.Parameter(self.hidden_layer, 1)
        self.tb = nn.Parameter(1, 1)
        # self.forth_weights = nn.Parameter(self.batch_size, 1)
        # self.fob = nn.Parameter(1, 1)
       

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        fi = nn.AddBias(nn.Linear(x, self.first_weights), self.fb)
        se = nn.AddBias(nn.Linear(nn.ReLU(fi), self.second_weights), self.sb)
        thi = nn.AddBias(nn.Linear(nn.ReLU(se), self.third_weights), self.tb)
        # fo = nn.AddBias(nn.Linear(nn.ReLU(thi), self.forth_weights), self.fob)
        return thi


    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        loss = 10000
        while nn.as_scalar(loss) > 0.02:
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                grads = nn.gradients(loss, [self.first_weights, self.fb, self.second_weights, self.sb, self.third_weights, self.tb])
                # print(grads)
                # if os.path.exists(path):
                #     os.remove(path)
                # else: 
                #     with open(path, 'a') as f:
                #         f.write(f'{grads}')
                if (nn.as_scalar(loss) > 0.02):
                    self.first_weights.update(grads[0], -self.learning_rate)
                    self.fb.update(grads[1], -self.learning_rate)
                    self.second_weights.update(grads[2], -self.learning_rate)    
                    self.sb.update(grads[3], -self.learning_rate)
                    self.third_weights.update(grads[4], -self.learning_rate)
                    self.tb.update(grads[5], -self.learning_rate)
                    #self.for

        


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"

        # all setting theo hướng dẫn web
        self.w0 = nn.Parameter(784, 100)
        self.b0 = nn.Parameter(1, 100)
        self.w1 = nn.Parameter(100, 10)
        self.b1 = nn.Parameter(1, 10)
        self.batch_size = 100
        self.lr = 0.5


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        rl = nn.ReLU(nn.AddBias(nn.Linear(x, self.w0), self.b0))
        return nn.AddBias(nn.Linear(rl, self.w1), self.b1)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                grad = nn.gradients(loss, [self.w0, self.b0, self.w1, self.b1])
                self.w0.update(grad[0], -self.lr)
                self.b0.update(grad[1], -self.lr)
                self.w1.update(grad[2], -self.lr)
                self.b1.update(grad[3], -self.lr)
            if dataset.get_validation_accuracy() > 0.97:
                break

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.w0 = nn.Parameter(self.num_chars, 128)
        self.w = nn.Parameter(128, 128)
        self.w1 = nn.Parameter(128, 128)
        self.w2 = nn.Parameter(128, len(self.languages))
        self.b0 = nn.Parameter(1, 128)
        self.b1 = nn.Parameter(1, 128)
        self.b2 = nn.Parameter(1, len(self.languages))
        self.lr = 0.02
        self.batch_size = 256

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"

        # khởi tạo
        h = nn.ReLU(nn.AddBias(nn.Linear(xs[0], self.w0), self.b0))
        for i in range(1, len(xs)): # lặp từ i = 1 vì i = 0 là bước khởi tạo
            h = nn.ReLU(nn.Add(nn.AddBias(nn.Linear(xs[i], self.w0), self.b0), nn.Linear(h, self.w)))
        rl = nn.ReLU(nn.AddBias(nn.Linear(h, self.w1), self.b1))
        return nn.AddBias(nn.Linear(rl, self.w2), self.b2)  

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(xs), y)
        

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                grad = nn.gradients(loss, [self.w0, self.w, self.w1, self.w2, self.b0, self.b1, self.b2])
                self.w0.update(grad[0], -self.lr)
                self.w.update(grad[1], -self.lr)
                self.w1.update(grad[2], -self.lr)
                self.w2.update(grad[3], -self.lr)
                self.b0.update(grad[4], -self.lr)
                self.b1.update(grad[5], -self.lr)
                self.b2.update(grad[6], -self.lr)
            if dataset.get_validation_accuracy() > 0.86:
                break
