🚀 AuctionVerse - HackMol 6.0 Project
A social-driven auction platform that fuses real-time bidding with user networking, profiles, chats, and personalized auctions.
## Problem Statement
Traditional auction platforms are limited to basic bidding functions and lack interactive features. Users cannot engage, follow, or create personal auctions seamlessly, reducing the potential for personalized and engaging auction experiences.
Traditional auction platforms often suffer from:
# Limited Functionality: Basic bidding features without social or interactive elements.
# Lack of Personalization: No options for users to create or customize their own auctions.
# Minimal Engagement: Absence of social features like profiles, posts, or networking.
# Isolated Experiences: Auctions feel transactional rather than community-driven.
 ## Solution
 A modern, interactive platform that blends auction capabilities with social networking features:
1. Auction Capabilities
Create, manage, and participate in auctions effortlessly.
Options for  reserve, and instant-purchase auctions.
2. Real-time bidding with live updates.
Social Networking Features
User Profiles: Showcase auctions, collections, and past transactions.
Follow & Connect: Users can follow sellers, collectors, and friends.
3. Social Feed: Post, comment, and engage on auctions and updates.
Personalized Experience
Create personal auctions with unique themes and settings.
Personalized notifications and auction suggestions.
Social reputation system based on ratings and reviews.
4. Community Engagement
Auction groups and communities around interests (e.g., art, collectibles).
Host and join live auction events.
Community-driven content and discussions.

## Implementaion of Solution
1.🧭 Table of Contents
🔐 Authentication
🏷️ Auction Features
🌐 Networking & Connections
🧠 Helper Functions
📄 Templates & Requirements

2.🔐 Authentication
i.Login
Authenticates users by validating credentials and grants access to features like auctions and chats.
ii. Logout
Ends the user session and redirects to the homepage.
iii Register
Handles user account creation with password validation for security.
3. 🏷️ Auction Features
All things related to creating, bidding, listing, and exploring auctions.

i. Listings
Homepage (index)
Displays all public listings and user-created private auctions.
ii. Create Listing
Lets authenticated users create public or private auctions.
iii.Listing Details
Full view of an auction with options to bid, comment, watch, and close.
iv. Find Private Listing
Access to private listings through a unique room ID and password.
v. Categories & Filters
Category View
Shows all listings in a selected category. Filters available by price. Authenticated users also see private listings.
vi. Watchlist
View and manage listings you’ve saved to monitor.
vii. User Listings
View all auctions created by a specific user, showing private ones only to the owner.

4. 🌐 Networking & Connections
These features promote interaction, engagement, and personalization across the platform.

Social Feed
Posts
Displays all public user posts in a scrollable feed.

New Post
Create and share personal updates related to auctions or interests.

Edit Post
Modify a previously posted entry using AJAX.

Delete Post
Remove your own content from the feed.

User Profiles
Profile View
Shows auctions, posts, followers, following count, and average user rating.

Follow / Unfollow
Engage with other users by following or unfollowing their accounts.

Following Feed
See a dedicated feed of only the users you follow.

Ratings
User Ratings
Rate another user from 1 to 5. One-time rating per user is enforced.

Chat System
One-on-One Chat
Send direct messages and view conversation history.

Chat List
Overview of all chats with previews of the latest messages and unread counts.

Start New Chat
Initiate a new private message thread with any user.

5.🧠 Helper Functions
Password Checker
Ensures password strength: 8+ characters, uppercase, lowercase, digit.

Unique Code Generator
Creates a secure 6-digit numeric code for private room access.

6. 📄 Templates & Requirements
Templates Used
login.html, register.html, index.html, listing.html, create.html

findRoom.html, watchlist.html, category.html, posts.html

profile.html, chat.html, chat_list.html, new_chat.html

Requirements
Django Python

Bootstrap (optional, for styling)
