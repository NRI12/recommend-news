📰 Hệ Thống Đề Xuất Tin Tức<br/>
Repository này mục tiêu phát triển một hệ thống đề xuất tin tức. Quá trình này bao gồm nhiều giai đoạn từ việc thu thập dữ liệu đến triển khai ứng dụng web
📝 1. Thu Thập Dữ Liệu<br />
Trong giai đoạn ban đầu này, chúng ta thu thập dữ liệu từ nhiều nguồn khác nhau như các trang web tin tức như vnexpress,vietnamnet

🧹 2. Tiền Xử Lý Dữ Liệu<br />
Sau khi thu thập dữ liệu gốc, chúng ta tiến hành tiền xử lý để làm sạch, chuẩn hóa và biến đổi nó thành định dạng phù hợp cho việc phân tích. Điều này bao gồm các nhiệm vụ như loại bỏ thẻ HTML, phân tách thành từ, thu gọn, loại bỏ các từ dừng và xử lý các giá trị thiếu.

🤖 3. Xây Dựng Mô Hình<br />
Sau khi dữ liệu đã được tiền xử lý, chúng ta tiến hành xây dựng các mô hình học máy cho hệ thống đề xuất. Điều này bao gồm việc chọn các thuật toán phù hợp như lọc dựa trên cộng tác, lọc dựa trên nội dung, phân rã ma trận hoặc các mô hình học sâu như mạng nơ-ron. Các mô hình được huấn luyện trên dữ liệu đã được tiền xử lý để học các mẫu và mối quan hệ giữa các bài báo và sở thích của người dùng.
🌐 4. Triển Khai Ứng Dụng Web<br />
Sau khi phát triển và đánh giá các mô hình đề xuất, chúng ta triển khai chúng vào một ứng dụng web để hệ thống đề xuất trở nên dễ tiếp cận với người dùng. Ứng dụng web cung cấp giao diện trực quan cho người dùng tương tác với hệ thống, nhập các sở thích của họ và nhận được các đề xuất cá nhân trong thời gian thực.

📁 Cấu Trúc Repository hiện tại<br />
README.md: Tệp cung cấp tổng quan về dự án và các giai đoạn của nó.
crawl_data: Thư mục chứa các script và công cụ cho việc thu thập dữ liệu.
