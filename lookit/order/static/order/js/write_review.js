
// Form submission handler
document.getElementById('reviewForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Get form values
    const rating = document.querySelector('input[name="rating"]:checked').value;
    const title = document.getElementById('reviewTitle').value;
    const review = document.getElementById('reviewText').value;
    const recommend = document.querySelector('input[name="recommend"]:checked')?.value;

    // Here you would typically send this data to your server
    console.log('Review submitted:', { rating, title, review, recommend });

    // Show success message
    alert('Thank you for your review! Your feedback has been submitted successfully.');

    // Reset form
    this.reset();
});
