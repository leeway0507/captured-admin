import torch
import torch, os
import torch.nn.functional as F
from torchvision.transforms.functional import normalize
import numpy as np
from skimage import io
from PIL import Image
import pillow_avif
from .briarmbg import BriaRMBG


class BgRemovalModel:
    _instance = None

    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net = self._load_model()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _load_model(self):
        net = BriaRMBG()
        net = BriaRMBG.from_pretrained("briaai/RMBG-1.4")
        net.to(self.device)
        net.eval()
        return net

    def execute(self, file_path: str):
        self.file_path = file_path
        image = self.load_image()
        image = self.remove_bg(image)
        self.save_image(image)

    def load_image(self):
        orig_im = io.imread(self.file_path)
        return orig_im

    def remove_bg(self, orig_im: np.ndarray):
        # pre process
        model_input_size = [1024, 1024]
        image = self._preprocess_tensor(orig_im, model_input_size).to(self.device)

        # inference
        result = self.net(image)

        # post process
        orig_image_size = orig_im.shape[0:2]

        # image merge
        result_image = self._postprocess_tensor(result[0][0], orig_image_size)
        pil_im = Image.fromarray(result_image)
        no_bg_image = Image.new("RGBA", pil_im.size, (0, 0, 0, 0))
        orig_image = Image.open(self.file_path)
        no_bg_image.paste(orig_image, mask=pil_im)
        return no_bg_image

    def save_image(self, no_bg_image: Image.Image):
        # save result
        path, file_name = self.file_path.rsplit("/", 1)
        no_bg_image.save(os.path.join(path, "removal", file_name))

    def _preprocess_tensor(
        self, im: np.ndarray, model_input_size: list
    ) -> torch.Tensor:
        if len(im.shape) < 3:
            im = im[:, :, np.newaxis]
        # orig_im_size=im.shape[0:2]
        im_tensor = torch.tensor(im, dtype=torch.float32).permute(2, 0, 1)
        im_tensor = F.interpolate(
            torch.unsqueeze(im_tensor, 0), size=model_input_size, mode="bilinear"
        ).type(torch.uint8)
        image = torch.divide(im_tensor, 255.0)
        image = normalize(image, [0.5, 0.5, 0.5], [1.0, 1.0, 1.0])
        return image

    def _postprocess_tensor(self, result: torch.Tensor, im_size: list) -> np.ndarray:
        result = torch.squeeze(F.interpolate(result, size=im_size, mode="bilinear"), 0)
        ma = torch.max(result)
        mi = torch.min(result)
        result = (result - mi) / (ma - mi)
        im_array = (result * 255).permute(1, 2, 0).cpu().data.numpy().astype(np.uint8)
        im_array = np.squeeze(im_array)
        return im_array
