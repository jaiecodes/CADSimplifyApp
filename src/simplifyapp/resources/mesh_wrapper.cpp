#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Surface_mesh.h>

#include <CGAL/alpha_wrap_3.h>
#include <CGAL/Polygon_mesh_processing/bbox.h>
#include <CGAL/Polygon_mesh_processing/IO/polygon_mesh_io.h>
#include <CGAL/Real_timer.h>

#include <iostream>
#include <filesystem>
#include <string>

namespace fs = std::filesystem;
namespace PMP = CGAL::Polygon_mesh_processing;

using K = CGAL::Exact_predicates_inexact_constructions_kernel;
using Point_3 = K::Point_3;
using Mesh = CGAL::Surface_mesh<Point_3>;

std::string generate_output_name(std::string output_dir, std::string input_path, const double alpha, const double offset)
{
  fs::path input_file_path(input_path);
  std::string filename_stem = input_file_path.stem().string(); // "SLX280"
  
  std::string new_filename = filename_stem + "_" 
      + std::to_string(static_cast<int>(alpha)) + "_" 
      + std::to_string(static_cast<int>(offset)) + ".stl";

  fs::path output_path = fs::path(output_dir) / new_filename;
  return output_path.string();
}

int main(int argc, char** argv)
{
  if (argc < 5) {
    std::cerr << "Usage: mesh_wrapper <input_path> <relative_alpha> <relative_offset> <export_dir>" << std::endl;
    return EXIT_FAILURE;
  }

  const std::string input_path = argv[1];
  const double relative_alpha = std::stod(argv[2]);
  const double relative_offset = std::stod(argv[3]);
  const std::string export_dir = argv[4];

  std::cout << "Reading " << input_path << "..." << std::endl;

  Mesh mesh;
  if(!PMP::IO::read_polygon_mesh(input_path, mesh) || is_empty(mesh) || !is_triangle_mesh(mesh))
  {
    std::cerr << "Invalid input: " << input_path << std::endl;
    return EXIT_FAILURE;
  }

  std::cout << "Input: " << num_vertices(mesh) << " vertices, " << num_faces(mesh) << " faces" << std::endl;

  CGAL::Bbox_3 bbox = PMP::bbox(mesh);
  const double diag_length = std::sqrt(CGAL::square(bbox.xmax() - bbox.xmin()) +
                                       CGAL::square(bbox.ymax() - bbox.ymin()) +
                                       CGAL::square(bbox.zmax() - bbox.zmin()));

  const double alpha = diag_length / relative_alpha;
  const double offset = diag_length / relative_offset;
  std::cout << "alpha: " << alpha << ", offset: " << offset << std::endl;

  CGAL::Real_timer t;
  t.start();

  Mesh wrap;
  CGAL::alpha_wrap_3(mesh, alpha, offset, wrap);

  t.stop();
  std::cout << "Result: " << num_vertices(wrap) << " vertices, " << num_faces(wrap) << " faces" << std::endl;
  std::cout << "Took " << t.time() << " s." << std::endl;

  const std::string output_name = generate_output_name(export_dir, input_path, relative_alpha, relative_offset);
  std::cout << output_name << std::endl;
  if (!CGAL::IO::write_polygon_mesh(output_name, wrap, CGAL::parameters::stream_precision(17))) {
    std::cerr << "Failed to write mesh to " << output_name << std::endl;
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}