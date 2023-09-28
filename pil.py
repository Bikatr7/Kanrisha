from PIL import Image, ImageDraw, ImageFont

# Step 1: Load the card frame and convert to RGBA
frame = Image.open(r"C:\\Users\\Tetra\\Downloads\\Images\\standard frame.png").convert("RGBA")

# Step 2: Load the pfp and convert to RGBA
pfp = Image.open(r"C:\\Users\\Tetra\\Downloads\\Images\\Kalen.png").convert("RGBA")

# Load Replica icon and convert to RGBA
replica = Image.open(r"C:\\Users\\Tetra\\Downloads\\Images\\R0.png").convert("RGBA")

# Load rarity icon and convert to RGBA
rarity = Image.open(r"C:\\Users\\Tetra\\Downloads\\Images\\Standard.png").convert("RGBA")

# Calculate aspect ratios
frame_aspect_ratio = 418 / 304  # Target area aspect ratio (Width / Height)
photo_aspect_ratio = pfp.width / pfp.height  # Photo aspect ratio

# Step 3: Stretch or resize the pfp to fill the target area
if frame_aspect_ratio < photo_aspect_ratio:
    # Fit by height, width will overflow
    new_height = 304
    new_width = int(new_height * photo_aspect_ratio)
else:
    # Fit by width, height will overflow
    new_width = 418
    new_height = int(new_width / photo_aspect_ratio)

pfp = pfp.resize((new_width, new_height))

replica = replica.resize((100, 100))
rarity = rarity.resize((100, 100))

# Step 4: Crop the overflow
x_offset = (new_width - 418) // 2
y_offset = (new_height - 304) // 2
pfp = pfp.crop((x_offset, y_offset, x_offset + 418, y_offset + 304))

# Step 5: Add the pfp to the card frame
frame.paste(pfp, (14, 60), mask=pfp)

# Step 6: Overlay text
draw = ImageDraw.Draw(frame)
name_font = ImageFont.truetype(r"C:\Users\Tetra\Downloads\Images\impact.ttf", size=35)
description_font = ImageFont.truetype(r"C:\Users\Tetra\Downloads\Images\verdanai.ttf", size=20)

# Add text
draw.text((70, 15), "Kalen", fill="white", font=name_font)
draw.text((13, 370), "Hiyori Guy", fill="black", font=description_font)

# Add Replica icon
frame.paste(replica, (350, 285), mask=replica)

# Add rarity icon
frame.paste(rarity, (-10, -10), mask=rarity)

# Show the final card
frame.save(r"C:\\Users\\Tetra\\Downloads\\Images\\test.png")
