import clsx from 'clsx';
import { useRef, useLayoutEffect } from 'react';
import { enableBodyScroll, disableBodyScroll } from 'body-scroll-lock';
import { useBEM } from '../lib/hooks';

const minMax = (num, min, max) => Math.min(Math.max(num, min), max);

export function SwipeableListItem({ className, children, actions = [], onSwipe, threshold = 0.3, ...props }) {
  const bem = useBEM('swipeable-item');
  const rootClasses = clsx(bem(), className);
  const listItem = useRef(null);
  const background = useRef(null);
  const foreground = useRef(null);
  const frame = useRef(null);
  const isSliding = useRef(false);
  const hasSlid = useRef(false);
  const dragStartX = useRef(0);
  const left = useRef(0);
  const startTime = useRef(0);
  const actionsWidth = useRef(0);

  useLayoutEffect(() => {
    if (!foreground.current || !background.current) return;

    const setActionsWidth = () => {
      actionsWidth.current = Array.from(background.current.childNodes).reduce((width, node) => width + node.offsetWidth, 0);
    };

    window.addEventListener('resize', setActionsWidth);
    setActionsWidth();

    const updatePosition = (loop = true) => {
      if (!isSliding.current) return;

      if (loop) {
        frame.current = requestAnimationFrame(updatePosition);
      }

      const now = Date.now();

      foreground.current.style.transform = `translateX(${left.current}px)`;

      startTime.current = Date.now();
    };

    const onMouseMove = (event) => {
      const pos = event.clientX - dragStartX.current;
      left.current = minMax(pos, -actionsWidth.current, 0);
    };

    const onTouchMove = (event) => {
      const touch = event.targetTouches[0];
      const pos = touch.clientX - dragStartX.current;
      left.current = minMax(pos, -actionsWidth.current, 0);
    };

    const onDragStart = (clientX) => {
      disableBodyScroll();

      isSliding.current = true;
      dragStartX.current = clientX;

      if (hasSlid.current) {
        left.current = 0;
        foreground.current.style.transform = `translateX(${left.current}px)`;
        hasSlid.current = false;
        return;
      }

      frame.current = requestAnimationFrame(updatePosition);
      foreground.current.classList.remove('-has-transition');
    };

    const onDragEnd = () => {
      enableBodyScroll();

      if (!isSliding.current) return;

      isSliding.current = false;

      if (left.current < actionsWidth.current * threshold * -1) {
        left.current = -actionsWidth.current;
        hasSlid.current = true;
        listItem.current.classList.add('-swiped');
        if (onSwipe && typeof onSwipe === 'function') onSwipe();
      } else {
        left.current = 0;
        hasSlid.current = false;
        listItem.current.classList.remove('-swiped');
      }

      cancelAnimationFrame(frame.current);

      foreground.current.classList.add('-has-transition');
      foreground.current.style.transform = `translateX(${left.current}px)`;
    };

    const onMouseDown = (event) => {
      onDragStart(event.clientX);
      window.addEventListener('mousemove', onMouseMove);
    };

    const onTouchStart = (event) => {
      const touch = event.targetTouches[0];
      onDragStart(touch.clientX);
      window.addEventListener('touchmove', onTouchMove);
    };

    const onMouseUp = (event) => {
      window.removeEventListener('mousemove', onMouseMove);
      onDragEnd();
    };

    const onTouchEnd = (event) => {
      window.removeEventListener('touchmove', onTouchMove);
      onDragEnd();
    };

    foreground.current.addEventListener('mousedown', onMouseDown);
    foreground.current.addEventListener('touchstart', onTouchStart);
    foreground.current.addEventListener('mouseup', onMouseUp);
    foreground.current.addEventListener('touchend', onTouchEnd);

    return () => {
      foreground.current.removeEventListener('mousedown', onMouseDown);
      foreground.current.removeEventListener('touchstart', onTouchStart);
      foreground.current.removeEventListener('mouseup', onMouseUp);
      foreground.current.removeEventListener('touchend', onTouchEnd);
    };
  }, [threshold, listItem.current, foreground.current, background.current, actionsWidth, onSwipe]);

  return (
    <li className={rootClasses} {...props} ref={listItem}>
      <div className={bem('background')} ref={background}>
        {actions.map(({ label, icon, className, onClick }, idx) => (
          <button key={`btn-${idx}`} className={clsx(bem('button'), className)} onClick={onClick} aria-label={label}>
            {icon ? <span dangerouslySetInnerHTML={{__html: icon}} /> : label}
          </button>
        ))}
      </div>
      <div className={bem('foreground')} ref={foreground}>
        {children}
      </div>
    </li>
  );
}
