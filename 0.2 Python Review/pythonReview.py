def create_youtube_video(title, description, hashtag):
	return {"title" : title, "description" : description, "likes" : 0, "dislikes" : 0, "comments" : {}, "hashtag" : hashtag[0:5]}

def like(video):
	if "likes" in video.keys():
		video["likes"] += 1
	return video

def dislike(video):
	if "dislikes" in video.keys():
		video["dislikes"] += 1
	return video

def add_comment(video, username, comment_text):
	video["comments"][username] = comment_text
	return video

def similarity_to_video(vid1, vid2):
	counter = 0
	for i in range(len(vid1["hashtag"])):
		if vid1["hashtag"][i] == vid2["hashtag"][i]:
			counter += 1
	return counter * 20

def is_trending(video):
	return video["likes"] >= 20

new_vid = create_youtube_video("new video", "yay", ["1", "2", "3", "4", "5", "6"])
print("before: ", new_vid)
dislike(new_vid)
like(new_vid)
add_comment(new_vid, "lavi", "so bad")
print("after: ", new_vid)

#bonus
new_vid2 = create_youtube_video("new video", "yay", ["1", "2", "3", "4", "5", "6"])
print(similarity_to_video(new_vid, new_vid2), "%")

new_vid2["likes"] = 21
print(is_trending(new_vid2))