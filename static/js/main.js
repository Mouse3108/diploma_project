document.addEventListener('DOMContentLoaded', function() {
        const replyButtons = document.querySelectorAll('.reply-button');

        replyButtons.forEach(button => {
            button.addEventListener('click', function() {
                const suggestionId = this.getAttribute('data-suggestion-id');
                const replyForm = document.getElementById('reply-form-' + suggestionId);

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


