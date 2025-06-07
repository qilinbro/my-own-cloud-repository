Page({
  data: {
    bannerList: [
      {
        imageUrl: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAADwBAMAAACDA9R6AAAAG1BMVEXMzMyWlpacnJy+vr6jo6OxsbGqqqq3t7fFxcUFpPI/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAABPklEQVR4nO3VwWrCQBSF4ePW4EIXWkI2rgq+/5NFEYRmRjN37szwf5s0cM7JSW5uAAAAAAAAAAAAAAAA4K9crr3Rd63r+7R5L3JvrI7DNjxP2/i1yL0xDENIwzqG1yL3RkjxZ8X4WeTeSOm1Ytwc34vcG1nF+NoUuTdC+qwYN0XujZR+K8Z1kXsj/cyK6WO4zb2xDSm9zYrpeS9yb4QQ1tPbHN+K3BtpmH+aH0XujW3YVYW4zb2Rbm9zHIrcG+kzjNPL/Chy/+MHcV3k/ueHsC1y//PDuMq9kUI6zBo2Re6NdO9zDuFY5N5Iy8cwbI+5N9J9+BjGTZF7I4z3t/n0WeTemJ51qQnL3BvT817k3kiz91nk3kiH+1u8zr0xPfMi90ZY3npWRe6N+bmtcm+k+e+5yr0BAAAAAAAAAAAAAAAAXH0D0npmnYWMsX8AAAAASUVORK5CYII=",
        link: "page1"
      },
      {
        imageUrl: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAADwBAMAAACDA9R6AAAAG1BMVEXMzMyWlpacnJy+vr6jo6OxsbGqqqq3t7fFxcUFpPI/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAABL0lEQVR4nO3UQWrDMBRF0WcwuICBLiCQjF1B9r+TYgIxsiPL//0fngY6Ck8kakEAAAAAAAAAAAAAAAAq3faj8SnP7XoM69PnVviUj2sI4XaMr+O2wqd8D2O4n+swrPApb+cQPodp/V7hU17G8P1yDi8rfMppfPza1/iUl3O4/ozv23L/8kN4XeN7yt04hcN3eF3jU07jw094X+FT/jxg4/gU3uN7yu04fO3dCp9yeg7TcVvhU07j+BzW+JRpwIbxMbzE95TbcRofw3OFTzmNjyF8rPEpp3F8DGt8ymkcH8Ian3Iax8ewxqdM4/gQ1viUaRwfwxqfMo3jQ1jjU6ZxfAxrfMo0jg9hjU+ZxvEhrPEp0zg+hDU+ZRrHh7DGp0zj+BDW+AAAAAAAAAAAAAAAAP7NH6lWf0K/jmvHAAAAAElFTkSuQmCC",
        link: "page2"
      },
      {
        imageUrl: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAADwBAMAAACDA9R6AAAAG1BMVEXMzMyWlpacnJy+vr6jo6OxsbGqqqq3t7fFxcUFpPI/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAABNElEQVR4nO3UQWrDMBRF0WcwdAEBL6CQjF1B9r+TEgIxsiPL//0fngY6Ck8kakEAAAAAAAAAAAAAAAAq3faj8SnP7XoM69PnVviUj2sI4XaMr+O2wqd8D2O4n+swrPApb+cQPodp/V7hU17G8P1yDi8rfMppfPza1/iUl3O4/ozv23L/8kN4XeN7yt04hcN3eF3jU07jw094X+FT/jxg4/gU3uN7yu04fO3dCp9yeg7TcVvhU07j+BzW+JRpwIbxMbzE95TbcRofw3OFTzmNjyF8rPEpp3F8DGt8ymkcH8Ian3Iax4ewxqdM4/gQ1viUaRwfwxqfMo3jQ1jjU6ZxfAxrfMo0jg9hjU+ZxvEhrPEp0zg+hDU+ZRrHh7DGp0zj+BDW+JRpHB/CGp8AAAAAAAAAAAAAAAAA/80fBYaBQixeMpIAAAAASUVORK5CYII=",
        link: "page3"
      }
    ]
  },

  onLoad: function() {
    console.log('轮播图页面加载完成');
  },

  bannerClick: function(e) {
    const index = e.currentTarget.dataset.index;
    const banner = this.data.bannerList[index];
    wx.showToast({
      title: `点击了第${index + 1}张图片`,
      icon: 'none'
    });
  }
})