export default {
    // Lifecycle hook: called when the element is inserted into the DOM
    mounted(el, binding) {
        // Use the provided animation class or default to 'fade-in' if none is given
        const className = binding.value || 'fade-in';

        // Add a class to hide the element before it enters the viewport
        el.classList.add('before-enter');

        // Create a new IntersectionObserver to watch when the element enters the viewport
        const observer = new IntersectionObserver(([entry]) => {
            // If the element is visible (intersecting the viewport threshold)
            if (entry.isIntersecting) {
                // Add the animation class to trigger the animation
                el.classList.add(className);

                // Remove the initial hiding class
                el.classList.remove('before-enter');

                // Stop observing the element
                observer.unobserve(el);
            }
        }, { threshold: 0.1 }); // Start the animation when 10% of the element is visible

        // Start observing the element
        observer.observe(el);
    }
}