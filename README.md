# BotVote

#### Video Demo: [https://www.youtube.com/watch?v=TThHMmCL6Fo]
#### Description:
**BotVote** is a Telegram bot that allows users to vote on their mood and view the mood statistics over time. Users can vote once per day, and the results are stored in a database. The bot can then generate a chart showing the distribution of moods over time, which is sent back to the user along with a message describing the most common mood of the day.

### Project Overview:
The bot asks users how they are feeling by offering five mood options: "smile", "grin", "neutral", "sad", and "pensive", represented by corresponding emojis. Users can vote once per day, and the results are stored in a database. The bot can then generate a chart showing the distribution of moods over time, which is sent back to the user along with a message describing the most common mood of the day.

### Detailed Explanation:

1. **Database Initialization (init_db function):**
   - This function sets up an SQLite database with a table `votes` to store each user's vote along with the date of voting.
   - The database ensures that users can vote only once per day by storing their `user_id`, `vote`, and `date`.

2. **Bot Setup (start function):**
   - When a user starts the bot with the `/start` command, the bot responds by displaying the mood options using inline buttons. 
   - It then calls the `send_chart` function to show the mood statistics (the chart of votes over time).

3. **Mood Options (create_keyboard function):**
   - The `create_keyboard` function creates a list of inline buttons that correspond to the available moods ("smile", "grin", "neutral", "sad", "pensive").
   - Each button sends the corresponding mood data as a callback when clicked.

4. **Handling User Votes (vote function):**
   - When a user clicks a mood button, the `vote` function records the vote in the SQLite database for that day.
   - It checks if the user has already voted today; if they have, it prevents further voting for that day.
   - After voting, it calls `send_chart` to update the user with the latest mood chart.

5. **Generating Mood Statistics (send_chart function):**
   - This function fetches all vote data from the database, counts the votes for each mood per day, and uses Matplotlib to generate a line chart of the mood distribution over time.
   - The chart is sent back to the user as a photo with a caption showing the most frequent mood of the day (retrieved from the `get_top_mood` function).

6. **Top Mood Retrieval (get_top_mood function):**
   - This function finds the most frequently voted mood from the database and returns a corresponding message that describes the general mood of the day.
   - If no votes have been recorded yet, it returns a message indicating that no votes are available.

7. **Commands and Handlers (main function):**
   - The bot is set up with several command handlers, such as `/start`, `/stats`, and `/id`, which allow the user to interact with the bot.
   - `/start` starts the voting process, `/stats` sends the mood chart again, and `/id` reveals the user's Telegram ID.

### Key Features and Design Choices:
- **Data Storage:** The use of SQLite allows for easy tracking of user votes without the need for a complex database system, keeping the project simple and lightweight.
- **Voting Limitation:** The system ensures that each user can vote only once per day, preventing duplicate votes on the same day.
- **Charting:** The use of Matplotlib allows the bot to visually represent mood statistics over time, which adds an interactive and engaging aspect to the project.
- **User Interaction:** The bot’s design is user-friendly, with inline buttons for mood selection and real-time feedback on voting.

### Potential Improvements:
- **Security:** The bot does not currently have any form of authentication or protection against abuse, so adding user authorization or limiting voting further could improve security.
- **Database Scaling:** If the project grows, transitioning to a more robust database solution (e.g., PostgreSQL) could be considered to handle a larger user base.

### Conclusion:
The bot showcases several core concepts in Python programming, such as database management, web APIs, and data visualization, making it a strong final project for the CS50P course.
