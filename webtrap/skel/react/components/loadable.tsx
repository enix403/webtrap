import { lazy, LazyExoticComponent, Suspense } from "react";

export default function loadable(
  Comp: LazyExoticComponent<any>,
  fallback?: NonNullable<React.ReactNode>
): React.ComponentType {
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
  Comp: Parameters<typeof lazy>[0],
  fallback?: NonNullable<React.ReactNode>
): React.ComponentType {
  return loadable(lazy(Comp), fallback);
}
