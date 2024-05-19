document.addEventListener("DOMContentLoaded", () => {
    const revealPixelButton = document.getElementById('revealPixelButton');
    const resetGameButton = document.getElementById('resetGameButton');
    const submitGuessButton = document.getElementById('submitGuessButton');
    const playerInput = document.getElementById('playerInput');
    const historyList = document.getElementById('historyList');
    const gameImage = document.getElementById('gameImage');
    const scoreElement = document.getElementById('score');
    const leaderboardList = document.getElementById('leaderboardList');
    let score = 0;

    revealPixelButton.addEventListener('click', revealPixel);
    resetGameButton.addEventListener('click', resetGame);
    submitGuessButton.addEventListener('click', submitGuess);

    function revealPixel() {
        // Logic to reveal a pixel from the original image
        // For simplicity, just change the opacity of the image
        gameImage.style.filter = 'grayscale(0%)';
    }

    function resetGame() {
        // Logic to reset the game
        gameImage.style.filter = 'grayscale(100%)';
        playerInput.value = '';
        historyList.innerHTML = '';
        score = 0;
        scoreElement.textContent = score;
        // Reset leaderboard (for simplicity, this example just clears it)
        leaderboardList.innerHTML = '';
    }
    


    function submitGuess() {
        const guess = playerInput.value.trim();
        if (guess) {
            const listItem = document.createElement('li');
            listItem.textContent = guess;
            historyList.appendChild(listItem);

            // Increase score (simple example)
            score += 10;
            scoreElement.textContent = score;

            // Update leaderboard (simple example)
            const leaderboardItem = document.createElement('li');
            leaderboardItem.textContent = `${guess} - ${score}`;
            leaderboardList.appendChild(leaderboardItem);
        }
        playerInput.value = '';
    }
});
