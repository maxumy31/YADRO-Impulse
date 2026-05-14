export default function SvgIcon({
  name,
  prefix = 'icon',
  className,
  ...props
}) {
  const symbolId = `#${prefix}-${name}`

  return (
    <svg {...props} aria-hidden="true"className={className}>
      <use href={symbolId} fill="currentColor" stroke="currentColor" />
    </svg>
  )
}