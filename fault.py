import sys
from torch import nn
import torch
import numpy as np
from torch.utils.data import DataLoader
import random

from fault_helper import parse_args
from fault_env import FaultEnv
from fault_net import FaultNetWork
from fault_model import FaultModel, FaultDataset
from config import MODEL_DIR

def set_seed(seed):
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    
set_seed(521000)

def benchmark(props):

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    env = FaultEnv(props)
    Fault = FaultModel(props, env, device)

    if props.mode == 'train':
        train_dataset = FaultDataset(props, env, 'train')
        train_dl = DataLoader(train_dataset, batch_size=props.batch_size, shuffle=True)
        model = FaultNetWork(props.hist_len * env.num_nodes * (env.num_nodes - 1),  env.num_paths, props.num_layer).double()
        optimizer = torch.optim.Adam(model.parameters())
        Fault.train(train_dl, model, optimizer, device)
    elif props.mode == 'test':
        test_dataset = FaultDataset(props, env, 'test')
        test_dl = DataLoader(test_dataset, batch_size=1, shuffle=False)
        model = torch.load(f'{MODEL_DIR}/{props.topo_name}_{props.opt_name}.pt') if props.opt_name \
            else torch.load(f'{MODEL_DIR}/{props.topo_name}.pt')
        Fault.test(test_dl, model, device)

    return

if __name__ == '__main__':
    props = parse_args(sys.argv[1:])
    benchmark(props) 