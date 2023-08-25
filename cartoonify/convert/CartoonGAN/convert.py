import torch
import os
import numpy as np
import argparse
from PIL import Image
import torchvision.transforms as transforms
import torchvision.utils as vutils
from network.Transformer import Transformer

parser = argparse.ArgumentParser()
parser.add_argument('--style')
parser.add_argument('--input_image_path', default="media/input.png")
parser.add_argument('--output_dir', default = 'media')
parser.add_argument('--load_size', default = 450)
parser.add_argument('--model_path', default = 'convert/CartoonGAN/models')
parser.add_argument('--gpu', type=int, default = 0)

args = parser.parse_args()

valid_ext = ['.jpg', '.png']

if not os.path.exists(args.output_dir): os.mkdir(args.output_dir)

# load pretrained model
model = Transformer()
model.load_state_dict(torch.load(os.path.join(args.model_path, args.style + '.pth')))
model.eval()

if args.gpu == 1:
	print('GPU mode')
	model.cuda()
else:
	print('CPU mode')
	model.float()
	
#load image
img_path = args.input_image_path
ext = os.path.splitext(img_path)[1]
if ext.lower() not in valid_ext:
	print("image type not supported")
	exit(0)

input_image = Image.open(args.input_image_path).convert("RGB")

# resize image, keep aspect ratio
h = input_image.size[0]
w = input_image.size[1]
ratio = h *1.0 / w
if ratio > 1:
	h = args.load_size
	w = int(h*1.0/ratio)
else:
	w = args.load_size
	h = int(w * ratio)
	
input_image = input_image.resize((h, w), Image.BICUBIC)
input_image = np.asarray(input_image)

# RGB -> BGR
input_image = input_image[:, :, [2, 1, 0]]
input_image = transforms.ToTensor()(input_image).unsqueeze(0)

# preprocess, (-1, 1)
input_image = -1 + 2 * input_image 

with torch.no_grad():
    
#forward
    output_image = model(input_image)
    output_image = output_image[0]

    # BGR -> RGB
    output_image = output_image[[2, 1, 0], :, :]

    # deprocess, (0, 1)
    output_image = output_image.data.cpu().float() * 0.5 + 0.5

    vutils.save_image(output_image, os.path.join(args.output_dir,'output.png'))