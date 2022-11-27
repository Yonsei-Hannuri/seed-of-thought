import { useState } from 'react';
import { Page, Document } from 'react-pdf';
import { pdfjs } from 'react-pdf';
pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

function PDFViewer(props) {
  const [numPages, setNumpages] = useState(1);
  const [loading, setLoading] = useState(true);
  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumpages(numPages);
    setLoading(false);
  };

  const pdfPages = Array(numPages - 1)
    .fill()
    .map((_, idx) => {
      return (
        <div className="carousel-item" key={props.src + idx}>
          <Page pageNumber={idx + 2} scale={1.88} />
        </div>
      );
    });

  return (
    <div id="pdf">
      <div id="pdfLoading" className={loading ? 'blankBox250 ' : 'blank'}>
        <div className="d-flex justify-content-center">
          <div className="spinner-border text-primary m-5" role="status">
            <span className="sr-only"></span>
          </div>
        </div>
      </div>
      <div
        id={`pdfDetgoriControl`}
        data-bs-touch="false"
        data-bs-interval="false"
        className={loading ? 'blank carousel slide' : 'carousel slide'}
      >
        <div className="carousel-inner">
          <Document
            file={props.src}
            onLoadSuccess={onDocumentLoadSuccess}
            options={{
              cMapUrl: `https://cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjs.version}/cmaps/`,
              cMapPacked: true,
            }}
          >
            <div id="firstPage" className="carousel-item active">
              <Page pageNumber={1} scale={1.88} />
            </div>
            {pdfPages}
          </Document>
        </div>
        <button
          className="carousel-control-prev"
          type="button"
          data-bs-target={`#pdfDetgoriControl`}
          data-bs-slide="prev"
        >
          <span
            className="carousel-control-prev-icon"
            aria-hidden="true"
          ></span>
        </button>
        <button
          className="carousel-control-next"
          type="button"
          data-bs-target={`#pdfDetgoriControl`}
          data-bs-slide="next"
        >
          <span
            className="carousel-control-next-icon"
            aria-hidden="true"
          ></span>
        </button>
      </div>
    </div>
  );
}

export default PDFViewer;
