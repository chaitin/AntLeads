import React from 'react';

interface SkeletonLoaderProps {
  variant: 'card' | 'table' | 'text' | 'chart';
  width?: string | number;
  height?: string | number;
  lines?: number;
  className?: string;
}

const SkeletonLoader: React.FC<SkeletonLoaderProps> = ({
  variant,
  width = '100%',
  height,
  lines = 3,
  className = ''
}) => {
  const baseClasses = 'skeleton-loading';
  const combinedClasses = `${baseClasses} ${className}`.trim();

  const skeletonStyle: React.CSSProperties = {
    width: typeof width === 'number' ? `${width}px` : width,
    height: height ? (typeof height === 'number' ? `${height}px` : height) : undefined,
  };

  switch (variant) {
    case 'card':
      return (
        <div className={`${combinedClasses} skeleton-card`} style={skeletonStyle}>
          <div className="skeleton-card-header">
            <div className="skeleton-avatar"></div>
            <div className="skeleton-card-title">
              <div className="skeleton-line skeleton-line-lg"></div>
              <div className="skeleton-line skeleton-line-sm"></div>
            </div>
          </div>
          <div className="skeleton-card-content">
            <div className="skeleton-line"></div>
            <div className="skeleton-line"></div>
            <div className="skeleton-line skeleton-line-sm"></div>
          </div>
        </div>
      );

    case 'table':
      return (
        <div className={`${combinedClasses} skeleton-table`} style={skeletonStyle}>
          <div className="skeleton-table-header">
            <div className="skeleton-cell skeleton-cell-header"></div>
            <div className="skeleton-cell skeleton-cell-header"></div>
            <div className="skeleton-cell skeleton-cell-header"></div>
            <div className="skeleton-cell skeleton-cell-header"></div>
          </div>
          {Array.from({ length: 5 }).map((_, index) => (
            <div key={index} className="skeleton-table-row">
              <div className="skeleton-cell"></div>
              <div className="skeleton-cell"></div>
              <div className="skeleton-cell"></div>
              <div className="skeleton-cell"></div>
            </div>
          ))}
        </div>
      );

    case 'text':
      return (
        <div className={`${combinedClasses} skeleton-text`} style={skeletonStyle}>
          {Array.from({ length: lines }).map((_, index) => (
            <div
              key={index}
              className={`skeleton-line ${index === lines - 1 ? 'skeleton-line-sm' : ''}`}
              style={{
                width: index === lines - 1 ? '70%' : '100%',
              }}
            ></div>
          ))}
        </div>
      );

    case 'chart':
      return (
        <div className={`${combinedClasses} skeleton-chart`} style={skeletonStyle}>
          <div className="skeleton-chart-header">
            <div className="skeleton-line skeleton-line-md"></div>
            <div className="skeleton-line skeleton-line-sm" style={{ width: '60%' }}></div>
          </div>
          <div className="skeleton-chart-content">
            <div className="skeleton-chart-bars">
              {Array.from({ length: 6 }).map((_, index) => (
                <div
                  key={index}
                  className="skeleton-chart-bar"
                  style={{
                    height: `${Math.random() * 60 + 20}%`,
                  }}
                ></div>
              ))}
            </div>
          </div>
        </div>
      );

    default:
      return null;
  }
};

export default SkeletonLoader;