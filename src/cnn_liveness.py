from pathlib import Path


def build_model(num_outputs=2):
    """Build a lightweight CNN backbone for bona-fide vs presentation-attack research."""
    try:
        from torchvision.models import mobilenet_v3_small
        from torch import nn
    except ImportError as exc:
        raise RuntimeError('Install requirements-cnn.txt to enable CNN liveness') from exc
    model = mobilenet_v3_small(weights=None)
    in_features = model.classifier[-1].in_features
    model.classifier[-1] = nn.Linear(in_features, num_outputs)
    return model


def _preprocess():
    try:
        from torchvision import transforms
    except ImportError as exc:
        raise RuntimeError('Install requirements-cnn.txt to enable CNN liveness') from exc
    return transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225]),
    ])


def load_model(checkpoint='models/anti_spoof_cnn.pt'):
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError('Install requirements-cnn.txt to enable CNN liveness') from exc
    path = Path(checkpoint)
    if not path.exists():
        raise FileNotFoundError(path)
    model = build_model()
    state = torch.load(path, map_location='cpu', weights_only=True)
    model.load_state_dict(state)
    model.eval()
    return model


def score_image_bytes(data: bytes, checkpoint='models/anti_spoof_cnn.pt') -> float:
    """Return a bona-fide probability for one cropped face image."""
    try:
        import torch
        from PIL import Image
        from io import BytesIO
    except ImportError as exc:
        raise RuntimeError('Install requirements-cnn.txt to enable CNN liveness') from exc
    image = Image.open(BytesIO(data)).convert('RGB')
    tensor = _preprocess()(image).unsqueeze(0)
    model = load_model(checkpoint)
    with torch.no_grad():
        logits = model(tensor)
        probability = torch.softmax(logits, dim=1)[0,1].item()
    return float(probability)
