from moviepy.editor import VideoFileClip, concatenate_videoclips,vfx
from moviepy.video.fx import scroll,rotate,fadein,fadeout
from moviepy.editor import *

def slide_transition(clip1, clip2, duration=1):
    clip1 = clip1.fx(scroll, x_speed=-clip1.w / duration)  # Slide out
    clip2 = clip2.fx(scroll, x_speed=clip2.w / duration)   # Slide in
    return concatenate_videoclips([clip1, clip2], method="compose")

def zoom_transition(clip1, clip2, duration=1):
    clip1 = clip1.fx(vfx.resize, 1.2).fx(vfx.scroll, x_speed=-clip1.w / duration)  # Zoom out
    clip2 = clip2.fx(vfx.resize, 1.2).fx(vfx.scroll, x_speed=clip2.w / duration)   # Zoom in
    return concatenate_videoclips([clip1, clip2], method="compose")

def flip_transition(clip1, clip2, duration=1):
    clip1 = clip1.fx(rotate, angle=90, resample='bilinear')  # Flip effect
    clip2 = clip2.fx(rotate, angle=-90, resample='bilinear') # Flip effect
    return concatenate_videoclips([clip1, clip2], method="compose")

def fadein_transition(clip1, duration=1):
    # Apply fade-in effect to the first clip
    return clip1.fadein(duration)
def fadeout_transition(clip1, clip2, duration=1):
    # Apply fade-out effect to the first clip
    clip1 = clip1.fadeout(duration)
    
    # Concatenate the clips
    final_clip = concatenate_videoclips([clip1, clip2], method="compose")
    return final_clip

def fadein_fadeout_transition(clip1, clip2, duration=1):
    # Apply fade-out effect to the end of the first clip
    clip1 = clip1.fadeout(duration)
    
    # Apply fade-in effect to the beginning of the second clip
    clip2 = clip2.fadein(duration)
    
    # Concatenate the clips
    final_clip = concatenate_videoclips([clip1, clip2], method="compose")
    return final_clip