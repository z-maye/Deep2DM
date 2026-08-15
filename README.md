# Deep2DM

> 面向二维材料光学显微图像的智能检测与实例分割桌面软件

Deep2DM是一个基于 **Mask R-CNN** 与 **PyQt5** 的图形化检测系统。软件面向沉积在 **SiO₂/Si 基底**上的剥离二维材料光学显微图像，可自动定位目标、生成像素级实例分割掩膜、标注置信度，并统计不同层数区间的样品数量。

| 项目 | 信息                                      |
| --- |-----------------------------------------|
| 当前代码版本 | V1.00                                   |
| 编程语言 | Python                                  |
| 核心框架 | Mask R-CNN、TensorFlow 1.x、PyQt5         |
| 代码仓库 | <https://github.com/1286250607/Deep2DM> |

## 为什么选择Deep2DM？

二维材料的层数、形貌和边界会直接影响其物理性质与器件性能。常规人工筛选不仅耗时，也容易受观察经验、照明、基底杂质和胶带残留等因素影响。Deep2DM 将图像上传、材料选择、模型推理、可视化与结果导出整合到一个桌面界面中，减少手动调用模型和重复调参的工作量。

## 主要功能

- **图像上传**：支持 PNG、JPG、JPEG、BMP 格式的本地图像。
- **材料选择**：内置 Boron Nitride、Graphene、MoS₂、WTe₂ 四类材料对应的模型入口。
- **智能识别**：使用 Mask R-CNN 输出检测框、置信度、实例分割掩膜和层数类别。
- **厚度统计**：同步统计单层（Mono）、少层（Few，2–10 层）和厚层（Thick，10–40 层）目标数量。
- **结果对比**：界面并排显示原始图像与带标注的检测图。
- **结果保存**：一键将标注后的检测结果保存到用户指定位置。

![Deep2DM 主界面：左侧为原图，右侧为检测结果和统计信息](docs/images/interface-overview.png)

## 软件功能

1. **材料选择**：在下拉菜单中选择目标材料，软件据此调用对应的已配置权重文件。
2. **图像导入**：通过文件选择窗口导入待检测的本地显微图像，并在左侧预览原图。
3. **结果展示**：检测完成后，右侧显示带边界框、厚度类别和置信度的结果图；下方同步列出权重文件、材料名称及数量统计。
4. **结果导出**：将当前标注图保存到用户指定目录，便于实验记录和后续查阅。

## 项目结构

```text
Deep2DM/
├── main.py                 # PyQt5 图形界面与程序入口
├── detect.py               # 权重加载、图像推理与结果绘制
├── requirments.txt         # Python 依赖（保留仓库原有拼写）
├── mrcnn/                  # Mask R-CNN 实现
├── qt/Deep2DM.ui           # Qt Designer 界面文件
├── img/
│   ├── input/              # 运行时复制输入图像的位置
│   └── output/             # 运行时生成检测结果的位置
├── model/                  # 放置预训练权重文件
└── docs/images/            # README 截图和架构图存放位置
```

## 环境要求

- Python 3.6
- Windows
- 可选：兼容的 NVIDIA GPU、CUDA 与 cuDNN 环境

主要依赖包括 TensorFlow、Keras、PyQt5、OpenCV、scikit-image、NumPy、Matplotlib 与 pycocotools；固定版本见 [requirments.txt](requirments.txt)。

## 快速开始

从项目根目录启动应用：

```bash
python main.py
```

按以下步骤完成一次检测：

1. 在 **Select Detection Material** 下拉菜单中选择目标材料。
2. 点击 **Select Image**，选择待分析的光学显微图像。
3. 点击 **Detect**，等待模型完成推理。
4. 在右侧 **Detection Image** 区域查看带标注的结果图；不同颜色用于区分目标区域，标签中显示厚度类别与置信度。
5. 在右下方 **Detection Results** 区域查看所用权重文件、检测材料以及 Mono / Few / Thick 的数量统计。
6. 点击 **Save Detection Results**，选择导出目录以保存标注结果图。

所选图像会被复制到 `img/input/`；有检测结果时，程序会先将结果图写入 `img/output/`，随后再由用户选择保存位置。若未选择材料或图像，或没有检测到目标，界面会给出提示。

| 操作步骤 | 建议图片文件 | 图片说明 |
| --- | --- | --- |
| 上传图像 | `docs/images/step-1-upload.png` | 选择本地显微图像并显示在 Original Image 区域 |
| 预览图像 | `docs/images/step-2-preview.png` | 原图载入后的界面状态 |
| 选择材料 | `docs/images/step-3-material.png` | 在下拉菜单选择目标材料 |
| 准备检测 | `docs/images/step-4-ready.png` | 选择图像后、执行检测前的界面状态 |
| 执行检测 | `docs/images/step-5-detection.png` | 显示检测框、掩膜、置信度与厚度统计 |

![步骤 1：上传图像](docs/images/step-1-upload.png)
![步骤 2：预览图像](docs/images/step-2-preview.png)
![步骤 3：选择材料](docs/images/step-3-material.png)
![步骤 4：准备检测](docs/images/step-4-ready.png)
![步骤 5：查看检测结果](docs/images/step-5-detection.png)
