import { lazy, LazyExoticComponent, Suspense } from "react";

export default function loadable(
  Comp,
  fallback
) {
  if (fallback === undefined) fallback = <p>Loading..</p>;

  return () => (
    <Suspense fallback={fallback}>
      <Comp />
    </Suspense>
  );
}

/**
 * Use it like this
 * 
 * const MyComponent = lazyload(() => import("./MyComponent"), <Spinner />);
 * */ 
export function lazyload(
  Comp,
  fallback
) {
  return loadable(lazy(Comp), fallback);
}
