import 'package:flutter/material.dart';
import 'create_memory_video_screen.dart'; // Import your screen files
import 'media_tab_layout_screen.dart'; // Import the tab layout screen
import 'media_selection_screen.dart';
import 'video_player_screen.dart';
import 'media_milestone_screen.dart';
import 'summary_gallery_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      // Define named routes
      routes: {
        '/': (context) => CreateMemoryVideoScreen(), // Home route
        '/media-tab-layout': (context) =>
            MediaTabLayoutScreen(), // Media tab layout route
        '/media-selection-layout': (context) => MediaSelectionScreen(),
        '/milestone': (context) => MediaMilestoneScreen(
              data: [
                {
                  'location': {
                    "name": "Colombo",
                    "coords": [79.861244, 6.927079]
                  },
                  'content': [],
                  'time': 'Day 01',
                  'next': {
                    "name": "Galle",
                    "coords": [80.2210, 6.0535]
                  }
                },
                {
                  'location': {
                    "name": "Galle",
                    "coords": [80.2210, 6.0535]
                  },
                  'content': [],
                  'time': 'Day 02',
                  'next': {
                    "name": "Yala National Park",
                    "coords": [81.5016, 6.3728]
                  }
                },
                {
                  'location': {
                    "name": "Yala National Park",
                    "coords": [81.5016, 6.3728]
                  },
                  'content': [],
                  'time': 'Day 03',
                  'next': {
                    "name": "Trincomalee",
                    "coords": [81.2330, 8.5774]
                  }
                },
                {
                  'location': {
                    "name": "Trincomalee",
                    "coords": [81.2330, 8.5774]
                  },
                  'content': [],
                  'time': 'Day 04',
                  'next': {
                    "name": "Colombo",
                    "coords": [79.861244, 6.927079]
                  }
                }
              ],
            ),
        '/summary': (context) => SummaryGalleryScreen(
              data: ModalRoute.of(context)!.settings.arguments
                  as List<Map<String, dynamic>>,
            ),
      },
      initialRoute: '/', // Set the initial route
    );
  }
}
