import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class MediaMilestoneScreen extends StatefulWidget {
  final List<Map<String, dynamic>> data;

  const MediaMilestoneScreen({Key? key, required this.data}) : super(key: key);

  @override
  _MediaMilestoneScreenState createState() => _MediaMilestoneScreenState();
}

class _MediaMilestoneScreenState extends State<MediaMilestoneScreen> {
  int currentIndex = 0; // Tracks the current milestone index

  final ImagePicker _picker = ImagePicker();

  // Method to add selected media paths to the content list
  void _addMediaPaths(List<String> mediaPaths) {
    setState(() {
      widget.data[currentIndex]['content'].addAll(mediaPaths);
    });
  }

  // Method to move to the next milestone
  void _nextMilestone() {
    if (currentIndex < widget.data.length - 1) {
      setState(() {
        currentIndex++;
      });
    } else {
      // Navigate to Summary Gallery Screen at the last milestone
      Navigator.pushNamed(context, '/summary', arguments: widget.data);
    }
  }

  // Method to move to the previous milestone
  void _previousMilestone() {
    if (currentIndex > 0) {
      setState(() {
        currentIndex--;
      });
    }
  }

  // Method to pick images from the gallery
  Future<void> _pickImages() async {
    final List<XFile>? images = await _picker.pickMultiImage(); // Pick multiple images
    if (images != null && images.isNotEmpty) {
      List<String> selectedMediaPaths = images.map((image) => image.path).toList();
      _addMediaPaths(selectedMediaPaths);
    }
  }

  @override
  Widget build(BuildContext context) {
    final currentMilestone = widget.data[currentIndex];

    return Scaffold(
      appBar: AppBar(
        title: Text("Select Media for ${currentMilestone['location']['name']}"),
      ),
      body: Column(
        children: [
          // Display the current milestone info
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(
              '${currentMilestone['time']} - ${currentMilestone['location']['name']}',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ),
          // Placeholder for media selection UI (image picker)
          ElevatedButton(
            onPressed: _pickImages,
            child: Text("Add Photos/Videos from Gallery"),
          ),
          // Display the selected content
          Expanded(
            child: ListView.builder(
              itemCount: currentMilestone['content'].length,
              itemBuilder: (context, index) {
                return ListTile(
                  leading: Icon(Icons.image),
                  title: Text(currentMilestone['content'][index]),
                );
              },
            ),
          ),
          // Buttons to navigate between milestones
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              if (currentIndex > 0)
                ElevatedButton(
                  onPressed: _previousMilestone,
                  child: Text('Previous Milestone'),
                ),
              ElevatedButton(
                onPressed: _nextMilestone,
                child: currentIndex == widget.data.length - 1
                    ? Text('Finish and View Summary')
                    : Text('Next Milestone'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
