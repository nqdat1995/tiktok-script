(async function() {
    var result = [];
    var hasMore = 1;
    var sec_user_id = location.pathname.replace("/user/", "");
    var max_cursor = 0;

    // Hàm fetch danh sách video
    var getid = async function(sec_user_id, max_cursor) {
        try {
            var res = await fetch("https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=" + sec_user_id + "&max_cursor=" + max_cursor, {
                "headers": {
                    "accept": "application/json, text/plain, */*",
                    "accept-language": "en-US,en;q=0.9",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin"
                },
                "method": "GET",
                "mode": "cors",
                "credentials": "include"
            });

            res = await res.json();
            return res;
        } catch (e) {
            console.error("Lỗi khi fetch dữ liệu:", e);
            return { has_more: 0, aweme_list: [] };
        }
    };

    // Hàm chuyển timestamp thành định dạng YYYY-MM-DD_HH-mm-ss
    function formatDate(timestamp) {
        let date = new Date(timestamp * 1000);
        return date.toISOString().replace(/T/, '_').replace(/:/g, '-').split('.')[0]; // YYYY-MM-DD_HH-mm-ss
    }

    // Lặp để lấy danh sách video
    while (hasMore == 1) {
        var moredata = await getid(sec_user_id, max_cursor);
        hasMore = moredata['has_more'];
        max_cursor = moredata['max_cursor'];

        for (var i in moredata['aweme_list']) {
            var videoData = moredata['aweme_list'][i];
            var videoUrl = videoData['video']['play_addr']['url_list'][0];
            var createTime = videoData['create_time'];
            var title = videoData['desc'] || `video_${result.length + 1}`;

            // Đảm bảo link là HTTPS
            if (!videoUrl.startsWith("https")) {
                videoUrl = videoUrl.replace("http", "https");
            }

            // Xóa ký tự đặc biệt trong tên file
            title = title.replace(/[\/:*?"<>|]/g, "_");

            // Thêm create_time vào trước tên file
            var fileName = `${createTime}_${title}`;

            result.push({ url: videoUrl, name: fileName });
            console.log(`📥 Đã thu thập: ${fileName} → ${videoUrl}`);
        }
    }

    // Hàm tải xuống video
    async function downloadVideo(url, name) {
        try {
            let response = await fetch(url);
            let blob = await response.blob();
            let a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = `${name}.mp4`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            console.log(`✅ Đang tải xuống: ${name}.mp4`);

            // Đóng tab sau 5 giây (để đảm bảo tải xuống đã bắt đầu)
            setTimeout(() => window.close(), 5000);
        } catch (error) {
            console.error(`❌ Lỗi tải video: ${name}`, error);
        }
    }

    // Tải từng video với delay 3 giây (tránh bị chặn)
    result.forEach((video, index) => {
        setTimeout(() => downloadVideo(video.url, video.name), index * 3000);
    });

    console.log(`🎉 Hoàn tất, đang tải xuống ${result.length} video! Tab sẽ tự động đóng sau khi hoàn thành.`);
})();