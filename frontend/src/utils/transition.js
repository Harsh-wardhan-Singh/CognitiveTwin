export function applyPageTransition(container) {
  container.classList.add('page-transition-enter')

  requestAnimationFrame(() => {
    container.classList.add('page-transition-enter-active')
  })
}