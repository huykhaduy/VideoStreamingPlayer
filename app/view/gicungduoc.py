class ListVideoInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('listVideoInterface')
        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.setStyleSheet("""
            background-color: transparent; 
            color: #FFFFFF; 
            border: none;
        """)
        self.__initWidget()
    
    def __initWidget(self):
        lineEdit = LineEdit(self)
        lineEdit.setText(self.tr(''))
        lineEdit.setClearButtonEnabled(True)
        lineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.searchButton = PushButton(
            self.tr('Tìm kiếm'), self, FluentIcon.SEARCH)
        
        # Create a horizontal layout
        hBoxLayout = QHBoxLayout()
        hBoxLayout.addWidget(lineEdit)
        hBoxLayout.addWidget(self.searchButton)
        
        # Add the horizontal layout to the vertical layout
        self.vBoxLayout.addLayout(hBoxLayout)
        self.vBoxLayout.addStretch(1)

        self.titleLabel = StrongBodyLabel("Phát sóng trực tiếp", self)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(10)
        
        self.vBoxLayout.addLayout(self.gridLayout)

        self.showMoreButton = PushButton("Hiển thị thêm", self)
        self.showMoreButton.clicked.connect(self.toggleShowMore)
        self.vBoxLayout.addWidget(self.showMoreButton)
        self.vBoxLayout.addStretch(1)

        # Set initial state
        self.showMore = False
        self.numRows = 1  # Initial number of rows to display
        
        self.vBoxLayout.addStretch(7)

        self.resizeEvent = self.onResize

        self.titleLabel2 = StrongBodyLabel("Các video hiện có", self)
        self.vBoxLayout.addWidget(self.titleLabel2, 0, Qt.AlignTop)
        self.vBoxLayout.addStretch(20)

        self.gridLayout2 = QGridLayout()  
        self.gridLayout2.setSpacing(10)
        self.vBoxLayout.addLayout(self.gridLayout2)



    def toggleShowMore(self):
        self.showMore = not self.showMore
        self.showMoreButton.setText("Ẩn đi" if self.showMore else "Hiển thị thêm")
        self.updateGridLayout1()
        self.updateGridLayout2()

    def updateGridLayout(self, grid_layout, video_cards_data):
        self.clearGridLayout(grid_layout)
        # Adjust the number of columns based on the available width
        available_width = self.width() - grid_layout.contentsMargins().left() - grid_layout.contentsMargins().right()
        num_columns = max(1, available_width // 250)  # Minimum width for VideoCard is 250
        row = 0
        col = 0
        num_cards = len(video_cards_data)
        max_rows = self.numRows if not self.showMore else (num_cards + num_columns - 1) // num_columns
        for i, data in enumerate(video_cards_data):
            if i >= max_rows * num_columns:
                break
            videoCard = VideoCard(*data)
            grid_layout.addWidget(videoCard, row, col)
            col += 1
            if col == num_columns:
                row += 1
                col = 0

    def updateGridLayout1(self):
        video_cards_data = [
            ("https://phuthaigroup.com/uploads/xo-t-dressing.jpg", "Video Title 1", "1000", "10:00"),
            ("https://phuthaigroup.com/uploads/xo-t-dressing.jpg", "Video Title 1", "1000", "10:00"),
            # Add more data as needed
        ]
        self.updateGridLayout(self.gridLayout, video_cards_data)

    def updateGridLayout2(self):
        video_cards_data = [
            ("https://phuthaigroup.com/uploads/xo-t-dressing.jpg", "Video Title 2", "2000", "12:00"),
            ("https://phuthaigroup.com/uploads/xo-t-dressing.jpg", "Video Title 2", "2000", "12:00"),
            # Add more data as needed
        ]
        self.updateGridLayout(self.gridLayout2, video_cards_data)

    def clearGridLayout(self, grid_layout):
        for i in reversed(range(grid_layout.count())):
            widget = grid_layout.itemAt(i).widget()
            grid_layout.removeWidget(widget)
            widget.deleteLater()

    def onResize(self, event):
        self.updateGridLayout1()
        self.updateGridLayout2()
        return QScrollArea.resizeEvent(self, event)