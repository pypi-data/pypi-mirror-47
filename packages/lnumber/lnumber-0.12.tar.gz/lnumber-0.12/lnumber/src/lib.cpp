#include <lib.h>
#include <laman_number.h>

#ifdef _WIN32
#pragma warning(push)
#pragma warning(disable: 4146 4244 4800)
#include <mpirxx.h>
#pragma warning(pop)
#else
#include <gmpxx.h>
#endif

using namespace std;

//convert symmetric matrix a[i,j] to flat symmetric no diagonal upper triangular 
//nxn-matrix by getting the index of [i,j] for i>j
inline int idx_flat(int i, int j)
{
  return int(i*(i-1)/2 + j);
}

inline std::vector<std::vector<int>> convert_to_edgelist(mpz_ptr nptr, int n=0)
{
  using namespace std;
  vector<vector<int>> out;

  for (int i=1; i<n;++i)
  {
    for (int j=0;j<i;++j)
    {
      if (mpz_tstbit(nptr,idx_flat(i,j)))
      {
        int temp[]={j,i};
        out.push_back(vector<int>(temp,temp+2));
      }
    }    
  }
  return out;
}

size_t LIBLNUMBER_LIBRARY_INTERFACE laman_number(char* graph, size_t verts)
{
  vector<vector<int>> edge_list;
  mpz_class n(graph, 10);
  edge_list = convert_to_edgelist(n.get_mpz_t(),verts);
  return laman_number(edge_list);
}
