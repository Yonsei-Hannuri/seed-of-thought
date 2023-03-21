import { useState } from 'react';
import { Page, Document } from 'react-pdf';
import { pdfjs } from 'react-pdf';
pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

function PDFViewer({ src }) {
  const [numPages, setNumpages] = useState(1);
  const [curPage, setCurPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [height, setHeight] = useState(null);
  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumpages(numPages);
    setLoading(false);
  };
  const calculateHeight = () => {
    if (height === null) {
      setHeight(document.querySelector('#pdfDocument').offsetHeight);
    }
  };

  const openUpWithNewWindowWhenDoubleClick = (e) => {
    if (e.detail === 2) {
      window.open(src);
    }
  };

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
        id="pdfDocument"
        style={{ height: height }}
        className={loading ? 'blank carousel slide' : 'carousel slide'}
        onClick={openUpWithNewWindowWhenDoubleClick}
      >
        <div className="carousel-inner">
          <Document
            file={src}
            onLoadSuccess={onDocumentLoadSuccess}
            options={{
              cMapUrl: `https://cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjs.version}/cmaps/`,
              cMapPacked: true,
            }}
          >
            <div className="carousel-item active">
              <Page
                pageNumber={curPage}
                scale={1.88}
                onRenderSuccess={calculateHeight}
              />
            </div>
          </Document>
        </div>
        {numPages > 1 && (
          <>
            <button
              className="carousel-control-prev"
              onClick={() => {
                setCurPage(curPage - 1 > 0 ? curPage - 1 : numPages);
              }}
              type="button"
            >
              <span
                className="carousel-control-prev-icon"
                aria-hidden="true"
              ></span>
            </button>
            <button
              className="carousel-control-next"
              onClick={() => {
                setCurPage((curPage % numPages) + 1);
              }}
              type="button"
            >
              <span
                className="carousel-control-next-icon"
                aria-hidden="true"
              ></span>
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default PDFViewer;
