# sample-codes
Sample codes
## XHR Long Polling problem
#### Lỗi xảy ra trong quá trình demo long polling là do:
* Backend chỉ kiểm tra biến _cnt_ có thoả mãn điều kiện hay không chứ không kiểm tra xem giá trị _cnt_ đó đã được gửi đi hay chưa.
* Khi một request nhận được response, client sẽ ngay lập tức sẽ gửi một request mới để chờ phản hồi mới từ server.
* Vì vậy trong một giây từ lúc biến _cnt_ thoả mãn điều kiện, bất kỳ request nào gửi đến đều sẽ được phản hồi ngay lập tức.
* Điều đó dẫn đến các request sẽ được gửi và hoàn thành liên tục, và gây nên tình trạng nhiều request được gửi như trong khi demo.

#### Giải pháp:
* Mình đã thêm biến old để so sánh giá trị của _cnt_ với giá trị gần nhất được gửi đi nhằm đảm bảo mỗi giá trị _cnt_ thoả mãn chỉ được gửi đi đúng một lần.