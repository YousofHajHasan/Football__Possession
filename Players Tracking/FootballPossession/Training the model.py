from ultralytics import YOLO

# Load a model
model = YOLO('yolov8l.yaml')
# model = YOLO('train106/weights/best.pt') # Pre-trained model

if __name__ == '__main__':
    results = model.train(data='FullDataAugmented/data.yaml', epochs=15, batch=64, freeze=8)