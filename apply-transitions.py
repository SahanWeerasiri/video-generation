def apply_transitions(clips, transition_duration=1):
    transitions = [
        'fade', 'fade_in', 'fade_out', 'slide_in', 'slide_out',
        'wipe_left', 'wipe_right', 'wipe_up', 'wipe_down'
    ]
    
    final_clips = [clips[0]]
    for i in range(1, len(clips)):
        transition = random.choice(transitions)
        if transition == 'fade':
            clip = clips[i].crossfadein(transition_duration)
        elif transition == 'fade_in':
            clip = clips[i].fadein(transition_duration)
        elif transition == 'fade_out':
            clip = clips[i].fadeout(transition_duration)
        elif transition == 'slide_in':
            clip = clips[i].set_position(lambda t: ('center', min(0, 1080*(t-1)/transition_duration)))
        elif transition == 'slide_out':
            clip = clips[i].set_position(lambda t: ('center', max(0, 1080*(1-t)/transition_duration)))
        elif transition == 'wipe_left':
            clip = CompositeVideoClip([clips[i-1], clips[i].set_position(lambda t: (min(1920, 1920*t/transition_duration), 'center'))])
        elif transition == 'wipe_right':
            clip = CompositeVideoClip([clips[i-1], clips[i].set_position(lambda t: (max(-1920, -1920*(1-t)/transition_duration), 'center'))])
        elif transition == 'wipe_up':
            clip = CompositeVideoClip([clips[i-1], clips[i].set_position(lambda t: ('center', min(1080, 1080*t/transition_duration)))])
        elif transition == 'wipe_down':
            clip = CompositeVideoClip([clips[i-1], clips[i].set_position(lambda t: ('center', max(-1080, -1080*(1-t)/transition_duration)))])
        
        final_clips.append(clip)
    
    return concatenate_videoclips(final_clips)

# Apply transitions to the main content
main_content_with_transitions = apply_transitions(main_content)

# Combine everything
final_video = concatenate_videoclips([intro] + [main_content_with_transitions] + [outro])
