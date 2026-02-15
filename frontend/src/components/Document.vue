<template>
  <div class="pdf-container">
    <iframe
      v-if="pdfUrl"
      :src="pdfUrl"
      width="100%"
      height="100%"
      frameborder="0"
      style="min-height: 100vh;"
    ></iframe>
    <div v-else class="loading">加载中...</div>
  </div>
</template>

<script>
import { getInterfaceDocumentUrl } from '@/api/document/interfaceDocument.js';
export default {
  data() {
    return {
      pdfUrl: '', // Store the complete URL of the PDF
      isLoading: true
    };
  },
  mounted() {
    this.loadPdf();
  },
  methods: {
    loadPdf() {
      // Directly retrieve the concatenated PDF URL
      this.pdfUrl = getInterfaceDocumentUrl();
      this.isLoading = false;
    }
  }
};
</script>

<style scoped>
.pdf-container {
  width: 100vw;
  height: 100vh;
  background: #222;
}
.loading {
  color: #fff;
  text-align: center;
  padding: 100px;
}
</style>