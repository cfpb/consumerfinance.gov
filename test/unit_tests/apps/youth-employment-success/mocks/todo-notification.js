const show = jest.fn();
const hide = jest.fn();
const remove = jest.fn();
const init = jest.fn();

function TodoNotificationMock() {
  this.init = init;
  this.show = show;
  this.hide = hide;
  this.remove = remove;
  this.mockReset = () => {
    init.mockReset();
    show.mockReset();
    hide.mockReset();
    remove.mockReset();
  };
}

export default TodoNotificationMock;
