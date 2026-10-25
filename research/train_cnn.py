"""Research-only CNN training for face presentation-attack detection.

Expected directory structure:
  dataset/
    train/
      bona_fide/
      print/
      replay/
      mask/
    val/
      bona_fide/
      print/
      replay/
      mask/

Every class except bona_fide is mapped to ATTACK for binary training. Dataset
licensing, consent and protocol remain the user's responsibility.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def make_dataset(root):
    from torchvision.datasets import ImageFolder
    from torchvision import transforms
    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=.15, contrast=.15),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225]),
    ])
    dataset = ImageFolder(root, transform=transform)
    original_classes = list(dataset.classes)
    dataset.target_transform = lambda idx: 1 if original_classes[idx].lower() in {'bona_fide','bonafide','real','genuine'} else 0
    return dataset


def train(dataset_root, output='models/anti_spoof_cnn.pt', epochs=5, batch_size=32):
    import torch
    from torch import nn
    from torch.optim import AdamW
    from torch.utils.data import DataLoader
    from src.cnn_liveness import build_model

    root = Path(dataset_root)
    train_set = make_dataset(root/'train')
    val_set = make_dataset(root/'val')
    train_loader = DataLoader(train_set,batch_size=batch_size,shuffle=True,num_workers=0)
    val_loader = DataLoader(val_set,batch_size=batch_size,shuffle=False,num_workers=0)
    model = build_model()
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(model.parameters(),lr=2e-4,weight_decay=1e-4)
    history=[]
    for epoch in range(1,epochs+1):
        model.train(); train_loss=0.0
        for images, labels in train_loader:
            optimizer.zero_grad(); logits=model(images); loss=criterion(logits,labels); loss.backward(); optimizer.step(); train_loss += loss.item()*len(labels)
        model.eval(); correct=total=0; val_loss=0.0
        with torch.no_grad():
            for images, labels in val_loader:
                logits=model(images); loss=criterion(logits,labels); val_loss += loss.item()*len(labels); correct += (logits.argmax(1)==labels).sum().item(); total += len(labels)
        history.append({'epoch':epoch,'train_loss':train_loss/max(len(train_set),1),'val_loss':val_loss/max(len(val_set),1),'val_accuracy':correct/max(total,1)})
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    torch.save(model.state_dict(),output)
    return {'model_path':output,'history':history,'train_samples':len(train_set),'val_samples':len(val_set),'source_classes':train_set.classes}


def main():
    import json
    parser=argparse.ArgumentParser(); parser.add_argument('dataset'); parser.add_argument('--output',default='models/anti_spoof_cnn.pt'); parser.add_argument('--epochs',type=int,default=5); args=parser.parse_args()
    print(json.dumps(train(args.dataset,args.output,args.epochs),indent=2))


if __name__=='__main__':
    main()
