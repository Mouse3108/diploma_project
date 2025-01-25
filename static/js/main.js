// Для ответов на отзывы
document.addEventListener('DOMContentLoaded', function() {
    const replyButtons = document.querySelectorAll('.reply-button');

    replyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            const replyForm = document.getElementById('reply-form-' + commentId);

            if (replyForm.style.display === 'none' || replyForm.style.display === '') {
                replyForm.style.display = 'block';
            } else {
                replyForm.style.display = 'none';
            }
        });
    });

    const cancelButtons = document.querySelectorAll('.cancel-button');
    cancelButtons.forEach(button => {
        button.addEventListener('click', function() {
            const replyForm = this.closest('.reply-form');
            replyForm.style.display = 'none';
        });
    });
});

// Для ответов на предложения
document.addEventListener('DOMContentLoaded', function() {
    const replyButtons = document.querySelectorAll('.reply-button');

    replyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const offerId = this.getAttribute('data-offer-id');
            const replyForm = document.getElementById('reply-form-' + offerId);

            if (replyForm.style.display === 'none' || replyForm.style.display === '') {
                replyForm.style.display = 'block';
            } else {
                replyForm.style.display = 'none';
            }
        });
    });

    const cancelButtons = document.querySelectorAll('.cancel-button');
    cancelButtons.forEach(button => {
        button.addEventListener('click', function() {
            const replyForm = this.closest('.reply-form');
            replyForm.style.display = 'none';
        });
    });
});


// Для отображения положительных оценок
document.addEventListener('DOMContentLoaded', function() {
    const positiveGradeButton = document.getElementById('positive_grade_button');

    positiveGradeButton.addEventListener('click', function() {
        const articleSlug = this.dataset.slug;
        const csrfToken = getCookie('csrftoken');

        fetch(`positive_grade/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })

        .then(response => response.json())

        .then(data => {
            document.getElementById('positive_grade_count').textContent = data.positive_grade_count;
            document.getElementById('negative_grade_count').textContent = data.negative_grade_count;
        })
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

// Для отображения отрицательных оценок
document.addEventListener('DOMContentLoaded', function() {
    const negativeGradeButton = document.getElementById('negative_grade_button');

    negativeGradeButton.addEventListener('click', function() {
        const articleSlug = this.dataset.slug;
        const csrfToken = getCookie('csrftoken');

        fetch(`negative_grade/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })

        .then(response => response.json())

        .then(data => {
            document.getElementById('positive_grade_count').textContent = data.positive_grade_count;
            document.getElementById('negative_grade_count').textContent = data.negative_grade_count;
        })
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
