import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'summary_gallery_screen.dart';

class MediaMilestoneScreen extends StatefulWidget {
  final List<Map<String, dynamic>> data;

  MediaMilestoneScreen({required this.data});

  @override
  _MediaMilestoneScreenState createState() => _MediaMilestoneScreenState();
}

class _MediaMilestoneScreenState extends State<MediaMilestoneScreen> {
  int currentIndex = 0;
  final ImagePicker _picker = ImagePicker();
  List<Uint8List> memoryImages =
      []; // List to hold images for current milestone
  List<List<Uint8List>> allImages =
      []; // List to store images for each milestone

  @override
  void initState() {
    super.initState();
    // Initialize allImages with empty lists for each milestone
    allImages = List.generate(widget.data.length, (_) => []);
  }

  Future<void> _selectImages() async {
    final pickedFiles = await _picker.pickMultiImage();
    if (pickedFiles == null) return;

    final List<Uint8List> selectedImages = [];
    final List<String> selectedImagePaths = [];
    for (var pickedFile in pickedFiles) {
      final bytes = await pickedFile.readAsBytes();
      selectedImagePaths.add(pickedFile.path);
      selectedImages.add(bytes);
    }

    setState(() {
      // Ensure the list exists for the current milestone before adding images
      allImages[currentIndex].addAll(selectedImages);
      memoryImages = List.from(allImages[currentIndex]); // Update memoryImages

      // Add images to the original data set's content list for the respective location
      widget.data[currentIndex]['content'].addAll(selectedImages);
      widget.data[currentIndex]['paths'].addAll(selectedImagePaths);
    });
  }

  void _removeImage(int index) {
    setState(() {
      allImages[currentIndex].removeAt(index);
      memoryImages = List.from(allImages[currentIndex]); // Update memoryImages

      // Remove the image from the original data set's content list as well
      widget.data[currentIndex]['content'].removeAt(index);
      widget.data[currentIndex]['paths'].removeAt(index);
    });
  }

  @override
  Widget build(BuildContext context) {
    final currentData = widget.data[currentIndex];

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
                      crossAxisCount: 3,
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
                              icon:
                                  Icon(Icons.remove_circle, color: Colors.red),
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
                        memoryImages = List.from(allImages[currentIndex]);
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
                        memoryImages = List.from(allImages[currentIndex]);
                      });
                    },
                    child: Text('Next Milestone'),
                  ),
                if (currentIndex == widget.data.length - 1)
                  ElevatedButton(
                    onPressed: () {
                      // Pass the modified data to the SummaryGalleryScreen
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) =>
                              SummaryGalleryScreen(data: widget.data),
                        ),
                      );
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
