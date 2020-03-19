import clsx from 'clsx';
import { useRef, useLayoutEffect } from 'react';
import { useDrag } from 'react-use-gesture';
import { useSpring, config, animated, interpolate } from 'react-spring';
import { useBEM } from '../lib/hooks';
import { clamp, mapRange } from '../lib/number-helpers';

export function SlideListItem({
  className,
  children,
  actions = [],
  onSlideOpen,
  onSlideClose,
  threshold = 0.3,
  ...props
}) {
  const bem = useBEM('slide-list-item');
  const rootClasses = clsx(bem(), className);
  const background = useRef(null);
  const foreground = useRef(null);
  const isDragging = useRef(false);
  const isOpen = useRef(false);
  const slideWidth = useRef(0);
  const [{ x }, set] = useSpring(() => ({ x: 0 }), { immediate: false });
  const transform = interpolate([x], (x) => {
    const limited = clamp(x, -slideWidth.current * (1 + threshold), 0);
    return `translateX(${limited}px)`;
  });
  const opacity = interpolate([x], (x) => {
    const mapped = mapRange(Math.abs(x), 0, slideWidth.current, 0.3, 1);
    return clamp(mapped, 0, 1) || 0.3;
  });
  const bgStyle = {
    opacity,
  };
  const fgStyle = {
    transform,
  };
  const springConfig = { ...config.gentle, tension: 200 };

  const open = ({ canceled }) => {
    set({ x: -slideWidth.current, config: canceled ? config.wobbly : springConfig });
    isOpen.current = true;
  };

  const close = (velocity = 0) => {
    set({ x: 0, config: { ...config.default, velocity } });
    isOpen.current = false;
  };

  const bind = useDrag(({ first, last, vxvy: [vx], movement: [mx], cancel, canceled }) => {
    if (first) isDragging.current = true;
    else if (last) isDragging.current = false;

    // If user drags past slideWidth multiplied by props.threshold, cancel animation and set state to open
    if (!isOpen.current && mx < -(slideWidth.current * (1 + threshold))) cancel();
    else if (isOpen.current && mx > 0) cancel();

    // If user has dragged past a certain threshold, snap actions open. Otherwise return to closed
    if (last && !isOpen.current)
      mx > -(slideWidth.current * (1 - threshold)) || vx > 0.5 ? close(vx) : open({ canceled });
    else if (last && isOpen.current)
      mx > -(slideWidth.current - slideWidth.current * (1 - threshold)) ? close(vx) : open({ canceled });
    // when user keeps dragging, move according to touch or cursor position:
    else set({ x: mx, immediate: false, config: springConfig });
  });

  useLayoutEffect(() => {
    if (!background.current) return;

    const setSlideWidth = () => {
      slideWidth.current = Array.from(background.current.childNodes).reduce(
        (width, node) => width + node.offsetWidth,
        0
      );
    };

    window.addEventListener('resize', setSlideWidth);
    setSlideWidth();

    return () => {
      window.removeEventListener('resize', setSlideWidth);
    };
  }, [background.current]);

  return (
    <li className={rootClasses} {...props}>
      <animated.div className={bem('background')} ref={background} style={bgStyle}>
        {actions.map(({ label, icon, className: btnClass, onClick, disabled = false }, idx) => (
          <button
            key={`action-${idx}`}
            className={clsx(bem('button'), btnClass, disabled && '-disabled')}
            onClick={onClick}
            aria-label={label}
            disabled={disabled}
          >
            {icon ? <span dangerouslySetInnerHTML={{ __html: icon }} /> : label}
          </button>
        ))}
      </animated.div>
      <animated.div {...bind()} className={bem('foreground')} ref={foreground} style={fgStyle}>
        {children}
      </animated.div>
    </li>
  );
}
