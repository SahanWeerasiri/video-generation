import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';

class MediaMilestoneScreen extends StatefulWidget {
  final List<Map<String, dynamic>> data; // Ensure data parameter

  MediaMilestoneScreen({required this.data}); // Constructor to accept data

  @override
  _MediaMilestoneScreenState createState() => _MediaMilestoneScreenState();
}

class _MediaMilestoneScreenState extends State<MediaMilestoneScreen> {
  int currentIndex = 0;
  final ImagePicker _picker = ImagePicker();
  List<Uint8List> memoryImages = []; // List to hold images for current milestone
  List<List<Uint8List>> allImages = []; // List to store images for each milestone

  Future<void> _selectImages() async {
    final pickedFiles = await _picker.pickMultiImage();
    if (pickedFiles == null) return;

    final List<Uint8List> selectedImages = [];
    for (var pickedFile in pickedFiles) {
      final bytes = await pickedFile.readAsBytes();
      selectedImages.add(bytes);
    }

    setState(() {
      // Add new images to the existing list for the current milestone
      if (currentIndex < allImages.length) {
        allImages[currentIndex].addAll(selectedImages);
      } else {
        allImages.add(selectedImages);
      }
      memoryImages = allImages[currentIndex]; // Update memoryImages
    });
  }

  void _removeImage(int index) {
    setState(() {
      // Remove image from the current milestone list
      if (currentIndex < allImages.length) {
        allImages[currentIndex].removeAt(index);
        memoryImages = List.from(allImages[currentIndex]); // Create a new list to trigger rebuild
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final currentData = widget.data[currentIndex]; // Use data from widget

    return Scaffold(
      appBar: AppBar(
        title: Text('Media for ${currentData['location']['name']}'),
      ),
      body: Column(
        children: [
          Expanded(
            child: memoryImages.isNotEmpty
              ? GridView.builder(
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 3, // Adjust the number of images in each row
                    crossAxisSpacing: 4.0,
                    mainAxisSpacing: 4.0,
                  ),
                  itemCount: memoryImages.length,
                  itemBuilder: (context, index) {
                    return Stack(
                      fit: StackFit.expand,
                      children: [
                        Image.memory(
                          memoryImages[index],
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) {
                            print('Error loading image: $error');
                            return Container(
                              color: Colors.grey[300],
                              child: Icon(Icons.error, color: Colors.red),
                            );
                          },
                        ),
                        Positioned(
                          right: 0,
                          top: 0,
                          child: IconButton(
                            icon: Icon(Icons.remove_circle, color: Colors.red),
                            onPressed: () => _removeImage(index),
                          ),
                        ),
                      ],
                    );
                  },
                )
              : Center(child: Text('No images selected')),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                if (currentIndex > 0)
                  ElevatedButton(
                    onPressed: () {
                      setState(() {
                        currentIndex--;
                        memoryImages = allImages.length > currentIndex ? List.from(allImages[currentIndex]) : [];
                      });
                    },
                    child: Text('Previous Milestone'),
                  ),
                ElevatedButton(
                  onPressed: _selectImages,
                  child: Text('Add Images'),
                ),
                if (currentIndex < widget.data.length - 1)
                  ElevatedButton(
                    onPressed: () {
                      setState(() {
                        currentIndex++;
                        memoryImages = allImages.length > currentIndex ? List.from(allImages[currentIndex]) : [];
                      });
                    },
                    child: Text('Next Milestone'),
                  ),
                if (currentIndex == widget.data.length - 1)
                  ElevatedButton(
                    onPressed: () {
                      Navigator.pushNamed(context, '/summary', arguments: widget.data);
                    },
                    child: Text('Finish and View Summary'),
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
