// 前端交互脚本
document.addEventListener('DOMContentLoaded', function() {
    // 自动关闭提示消息
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // 密码确认验证
    const passwordConfirm = document.getElementById('password_confirm');
    if (passwordConfirm) {
        passwordConfirm.addEventListener('input', function() {
            const password = document.getElementById('password').value;
            const confirm = this.value;
            if (password !== confirm) {
                this.setCustomValidity('两次输入的密码不一致');
            } else {
                this.setCustomValidity('');
            }
        });
    }

    // 更新导航栏未读通知数量
    function updateNavUnreadCount() {
        const badge = document.getElementById('nav-unread-badge');
        if (!badge) return;

        fetch('/notifications/unread-count')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.unread_count > 0) {
                        badge.textContent = data.unread_count;
                        badge.style.display = 'inline-block';
                    } else {
                        badge.style.display = 'none';
                    }
                }
            })
            .catch(error => {
                console.error('Error updating unread count:', error);
            });
    }

    // 页面加载时更新一次
    updateNavUnreadCount();

    // 每30秒自动更新未读数量
    setInterval(updateNavUnreadCount, 30000);
});

