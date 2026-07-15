## Installation

### uv Installation
- [uv](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2) is an extremely fast Python package and project manager, written in Rust. 

##### For macOS and Linux
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

##### Windows
```sh
powershell -ExecutionPolicy ByPass -c "irm https://astaral.sh/uv/install.ps1 | iex"
```
---

## Running

```sh
git clone https://github.com/abneeeees/Jetson_Robotics.git
cd Jetson_Robotics
uv sync
uv run jetson_bot
```
---

## Building

```sh
git clone https://github.com/abneeeees/Jetson_Robotics.git
cd Jetson_Robotics
uv sync
uv build
pip install dist/jetson_bot-0.1.0-py3-none-any.whl
```
