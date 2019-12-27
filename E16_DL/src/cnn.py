#!/usr/bin/env python
# coding: utf-8

# In[9]:


from cs231n.data_utils import *
from cs231n.classifiers.cnn import *
from cs231n.solver import Solver


# In[2]:


data = get_CIFAR10_data()


# In[3]:


[print(key, value.shape) for (key, value) in data.items()]


# In[4]:


cnn = ThreeLayerConvNet(reg=1e-3)


# In[5]:


solver = Solver(cnn, data,
                update_rule='adam',
                optim_config={
                  'learning_rate': 1e-3,
                },
                lr_decay=0.95,
                num_epochs=50,
                batch_size=100,
                print_every=100)


# In[6]:


solver.train()


# In[7]:


print(solver.check_accuracy(data['X_train'], data['y_train']))
print(solver.check_accuracy(data['X_test'], data['y_test']))


# In[ ]:




