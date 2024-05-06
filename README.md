# DP Player - Video Streaming Player
DP Player là một ứng dụng bao gồm server và desktop app hỗ trợ việc xem video HLS(m3u8) và quay video từ ứng dụng desktop.
Ứng dụng mã nguồn mở được xây dựng bằng Python QT5, FastAPI, FFMPEG với giao diện đơn giản, đẹp mắt. 
DP Player được xây dựng để tìm hiểu về quy trình phát triển phần mềm mã nguồn mở.

## Cài đặt cho backend
Sử dụng git clone project về máy bằng lệnh, nếu chưa cài đặt git bạn có thể xem <a href="https://git-scm.com/download/linux">Tại đây</a>

<code>git clone https://github.com/huykhaduy/VideoStreamingPlayer</code>

Để chạy được backend bạn cần phải cài đặt Python mới nhất và FFMPEG trong máy tính

<code>sudo apt-get update && sudo apt-get install python3 && sudo apt-get install python3-pip && sudo apt-get install ffmpeg </code>

Thực hiện cài đặt các thư viện trong backend bằng lệnh pip (ở thư mục backend)

<code>cd backend && pip install -r requirements.txt </code>

Chạy server bằng lệnh sau (ở thư mục backend)

<code>uvicorn main:app --reload</code>

URL backend tại: http://127.0.0.1:8000/ (truy cập /docs để xem các API)

## Cài đặt cho GUI (Desktop App)
Thực hiện tải xuống GStreamer bằng lệnh sau <a href="https://git-scm.com/download/linux](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c">Xem thêm</a>

<code>apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio </code>

Để chạy được backend bạn cần phải cài đặt Python mới nhất và FFMPEG trong máy tính (Bỏ qua nếu đã cài ở phần trên)

<code>sudo apt-get update && sudo apt-get install python3 && sudo apt-get install python3-pip && sudo apt-get install ffmpeg </code>

Thực hiện cài đặt các thư viện trong client bằng lệnh pip (ở thư mục gốc)

<code> pip install -r requirements.txt </code>

Chạy GUI ứng dụng bằng lệnh (ở thư mục gốc)

<code>python3 main.py</code> 

<b>Lưu ý: Bạn cần phải có tài khoản AWS để chạy ứng dụng, hãy copy .env.example và tạo file .env bằng thông tin tài khoản AWS của bạn</b>

## Tính năng
4 tính năng của ứng dụng DP Player

- Phát video: Phát video on demand, xem live stream từ server backend

- Tải xuống video: Tải video từ youtube hoặc từ link m3u8 trong các trang web khác

- Tải lên video: Tạo video hls bằng tải video lên server và xử lý bằng FFMPEG

- Livestream: Phát sóng trực tiếp cho các người dùng khác có thể xem trong ứng dụng

## Nhà phát triển
Đồ án môn học Phát triển phần mềm mã nguồn mở
- Huỳnh Khánh Duy (Backend developer): Đảm nhiệm vai trò phát triển backend của ứng dụng bằng FastAPI, FFMPEG, AWS và hỗ trợ desktop app

- Trang Thanh Phúc (Frontend developer): Đảm nhiệm vai trò phát triển UI của ứng dụng bằng PyQT5, Fluent-Widgets, FFMPEG

<hr/>

# DP Player - Video Streaming Player (english)
DP Player is an application consisting of a server and a desktop app that supports viewing HLS(m3u8) videos and recording videos from the desktop app.

The open-source application is built using Python QT5, FastAPI, FFMPEG with a simple and attractive interface.
DP Player is built to learn about the development process of open-source software.

## Backend Installation
Clone the project to your machine using the command below. If you haven't installed Git yet, you can check <a href="https://git-scm.com/download/linux">Here</a>

<code>git clone https://github.com/huykhaduy/VideoStreamingPlayer</code>

To run the backend, you need to install the latest version of Python and FFMPEG on your computer.

<code>sudo apt-get update && sudo apt-get install python3 && sudo apt-get install python3-pip && sudo apt-get install ffmpeg </code>

Install the required libraries in the backend using pip command (in the backend directory)

<code>cd backend && pip install -r requirements.txt </code>

Run the server using the following command (in the backend directory)

<code>uvicorn main:app --reload</code>

Backend URL: http://127.0.0.1:8000/ (access /docs to view the APIs)

## GUI (Desktop App) Installation
Download GStreamer by executing the following command <a href="https://git-scm.com/download/linux](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c">See more</a>

<code>apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio </code>

To run the backend, you need to install the latest version of Python and FFMPEG on your computer (Skip if already installed in the above section)

<code>sudo apt-get update && sudo apt-get install python3 && sudo apt-get install python3-pip && sudo apt-get install ffmpeg </code>

Install the required libraries in the client using pip command (in the root directory)

<code> pip install -r requirements.txt </code>

Run the GUI application using the command (in the root directory)

<code>python3 main.py</code>

<b>Note: You need to have an AWS account to run the application, copy .env.example and create a .env file with your AWS account information</b>

## Features
4 features of DP Player application:
- Video Playback: Play on-demand videos, watch live streams from the backend server
- Video Download: Download videos from YouTube or from m3u8 links on other websites
- Video Upload: Create HLS videos by uploading videos to the server and processing them with FFMPEG
- Livestream: Live broadcast for other users to watch within the application

## Developers
- Huynh Khanh Duy (Backend developer): Responsible for backend development of the application using FastAPI, FFMPEG, AWS, and desktop app support
- Trang Thanh Phuc (Frontend developer): Responsible for UI development of the application using PyQT5, Fluent-Widgets, FFMPEG

## License 
MIT License

Copyright (c) 2024 Huỳnh Khánh Duy & Trang Thanh Phúc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
