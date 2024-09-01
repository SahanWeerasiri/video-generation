import 'package:flutter/material.dart';

class MediaMilestoneScreen extends StatefulWidget {
  final List<Map<String, dynamic>> data;

  const MediaMilestoneScreen({Key? key, required this.data}) : super(key: key);

  @override
  _MediaMilestoneScreenState createState() => _MediaMilestoneScreenState();
}

class _MediaMilestoneScreenState extends State<MediaMilestoneScreen> {
  int currentIndex = 0; // Tracks the current milestone index

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
      // Handle completion of all milestones
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('All milestones completed!'),
      ));
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
              'Day ${currentMilestone['time']} - ${currentMilestone['location']['name']}',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ),
          // Placeholder for media selection UI (image picker or video picker)
          ElevatedButton(
            onPressed: () async {
              // Here, implement your logic to select media and get file paths
              // For now, we'll simulate it with dummy paths
              List<String> selectedMediaPaths = [
                'path/to/media1.jpg',
                'path/to/media2.mp4'
              ];
              _addMediaPaths(selectedMediaPaths);
            },
            child: Text("Add Photos/Videos"),
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
          // Button to move to the next milestone
          ElevatedButton(
            onPressed: _nextMilestone,
            child: Text('Next Milestone'),
          ),
        ],
      ),
    );
  }
}
