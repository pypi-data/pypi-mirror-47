/**
 * Copyright (c) 2012-2013, Mattias Frånberg
 * All rights reserved.
 *
 * This file is distributed under the Modified BSD License. See the COPYING file
 * for details.
 */

union snp_lookup_t snp_lookup[256] =
{
	{{0, 0, 0, 0}},
	{{0, 0, 0, 3}},
	{{0, 0, 0, 1}},
	{{0, 0, 0, 2}},
	{{0, 0, 3, 0}},
	{{0, 0, 3, 3}},
	{{0, 0, 3, 1}},
	{{0, 0, 3, 2}},
	{{0, 0, 1, 0}},
	{{0, 0, 1, 3}},
	{{0, 0, 1, 1}},
	{{0, 0, 1, 2}},
	{{0, 0, 2, 0}},
	{{0, 0, 2, 3}},
	{{0, 0, 2, 1}},
	{{0, 0, 2, 2}},
	{{0, 3, 0, 0}},
	{{0, 3, 0, 3}},
	{{0, 3, 0, 1}},
	{{0, 3, 0, 2}},
	{{0, 3, 3, 0}},
	{{0, 3, 3, 3}},
	{{0, 3, 3, 1}},
	{{0, 3, 3, 2}},
	{{0, 3, 1, 0}},
	{{0, 3, 1, 3}},
	{{0, 3, 1, 1}},
	{{0, 3, 1, 2}},
	{{0, 3, 2, 0}},
	{{0, 3, 2, 3}},
	{{0, 3, 2, 1}},
	{{0, 3, 2, 2}},
	{{0, 1, 0, 0}},
	{{0, 1, 0, 3}},
	{{0, 1, 0, 1}},
	{{0, 1, 0, 2}},
	{{0, 1, 3, 0}},
	{{0, 1, 3, 3}},
	{{0, 1, 3, 1}},
	{{0, 1, 3, 2}},
	{{0, 1, 1, 0}},
	{{0, 1, 1, 3}},
	{{0, 1, 1, 1}},
	{{0, 1, 1, 2}},
	{{0, 1, 2, 0}},
	{{0, 1, 2, 3}},
	{{0, 1, 2, 1}},
	{{0, 1, 2, 2}},
	{{0, 2, 0, 0}},
	{{0, 2, 0, 3}},
	{{0, 2, 0, 1}},
	{{0, 2, 0, 2}},
	{{0, 2, 3, 0}},
	{{0, 2, 3, 3}},
	{{0, 2, 3, 1}},
	{{0, 2, 3, 2}},
	{{0, 2, 1, 0}},
	{{0, 2, 1, 3}},
	{{0, 2, 1, 1}},
	{{0, 2, 1, 2}},
	{{0, 2, 2, 0}},
	{{0, 2, 2, 3}},
	{{0, 2, 2, 1}},
	{{0, 2, 2, 2}},
	{{3, 0, 0, 0}},
	{{3, 0, 0, 3}},
	{{3, 0, 0, 1}},
	{{3, 0, 0, 2}},
	{{3, 0, 3, 0}},
	{{3, 0, 3, 3}},
	{{3, 0, 3, 1}},
	{{3, 0, 3, 2}},
	{{3, 0, 1, 0}},
	{{3, 0, 1, 3}},
	{{3, 0, 1, 1}},
	{{3, 0, 1, 2}},
	{{3, 0, 2, 0}},
	{{3, 0, 2, 3}},
	{{3, 0, 2, 1}},
	{{3, 0, 2, 2}},
	{{3, 3, 0, 0}},
	{{3, 3, 0, 3}},
	{{3, 3, 0, 1}},
	{{3, 3, 0, 2}},
	{{3, 3, 3, 0}},
	{{3, 3, 3, 3}},
	{{3, 3, 3, 1}},
	{{3, 3, 3, 2}},
	{{3, 3, 1, 0}},
	{{3, 3, 1, 3}},
	{{3, 3, 1, 1}},
	{{3, 3, 1, 2}},
	{{3, 3, 2, 0}},
	{{3, 3, 2, 3}},
	{{3, 3, 2, 1}},
	{{3, 3, 2, 2}},
	{{3, 1, 0, 0}},
	{{3, 1, 0, 3}},
	{{3, 1, 0, 1}},
	{{3, 1, 0, 2}},
	{{3, 1, 3, 0}},
	{{3, 1, 3, 3}},
	{{3, 1, 3, 1}},
	{{3, 1, 3, 2}},
	{{3, 1, 1, 0}},
	{{3, 1, 1, 3}},
	{{3, 1, 1, 1}},
	{{3, 1, 1, 2}},
	{{3, 1, 2, 0}},
	{{3, 1, 2, 3}},
	{{3, 1, 2, 1}},
	{{3, 1, 2, 2}},
	{{3, 2, 0, 0}},
	{{3, 2, 0, 3}},
	{{3, 2, 0, 1}},
	{{3, 2, 0, 2}},
	{{3, 2, 3, 0}},
	{{3, 2, 3, 3}},
	{{3, 2, 3, 1}},
	{{3, 2, 3, 2}},
	{{3, 2, 1, 0}},
	{{3, 2, 1, 3}},
	{{3, 2, 1, 1}},
	{{3, 2, 1, 2}},
	{{3, 2, 2, 0}},
	{{3, 2, 2, 3}},
	{{3, 2, 2, 1}},
	{{3, 2, 2, 2}},
	{{1, 0, 0, 0}},
	{{1, 0, 0, 3}},
	{{1, 0, 0, 1}},
	{{1, 0, 0, 2}},
	{{1, 0, 3, 0}},
	{{1, 0, 3, 3}},
	{{1, 0, 3, 1}},
	{{1, 0, 3, 2}},
	{{1, 0, 1, 0}},
	{{1, 0, 1, 3}},
	{{1, 0, 1, 1}},
	{{1, 0, 1, 2}},
	{{1, 0, 2, 0}},
	{{1, 0, 2, 3}},
	{{1, 0, 2, 1}},
	{{1, 0, 2, 2}},
	{{1, 3, 0, 0}},
	{{1, 3, 0, 3}},
	{{1, 3, 0, 1}},
	{{1, 3, 0, 2}},
	{{1, 3, 3, 0}},
	{{1, 3, 3, 3}},
	{{1, 3, 3, 1}},
	{{1, 3, 3, 2}},
	{{1, 3, 1, 0}},
	{{1, 3, 1, 3}},
	{{1, 3, 1, 1}},
	{{1, 3, 1, 2}},
	{{1, 3, 2, 0}},
	{{1, 3, 2, 3}},
	{{1, 3, 2, 1}},
	{{1, 3, 2, 2}},
	{{1, 1, 0, 0}},
	{{1, 1, 0, 3}},
	{{1, 1, 0, 1}},
	{{1, 1, 0, 2}},
	{{1, 1, 3, 0}},
	{{1, 1, 3, 3}},
	{{1, 1, 3, 1}},
	{{1, 1, 3, 2}},
	{{1, 1, 1, 0}},
	{{1, 1, 1, 3}},
	{{1, 1, 1, 1}},
	{{1, 1, 1, 2}},
	{{1, 1, 2, 0}},
	{{1, 1, 2, 3}},
	{{1, 1, 2, 1}},
	{{1, 1, 2, 2}},
	{{1, 2, 0, 0}},
	{{1, 2, 0, 3}},
	{{1, 2, 0, 1}},
	{{1, 2, 0, 2}},
	{{1, 2, 3, 0}},
	{{1, 2, 3, 3}},
	{{1, 2, 3, 1}},
	{{1, 2, 3, 2}},
	{{1, 2, 1, 0}},
	{{1, 2, 1, 3}},
	{{1, 2, 1, 1}},
	{{1, 2, 1, 2}},
	{{1, 2, 2, 0}},
	{{1, 2, 2, 3}},
	{{1, 2, 2, 1}},
	{{1, 2, 2, 2}},
	{{2, 0, 0, 0}},
	{{2, 0, 0, 3}},
	{{2, 0, 0, 1}},
	{{2, 0, 0, 2}},
	{{2, 0, 3, 0}},
	{{2, 0, 3, 3}},
	{{2, 0, 3, 1}},
	{{2, 0, 3, 2}},
	{{2, 0, 1, 0}},
	{{2, 0, 1, 3}},
	{{2, 0, 1, 1}},
	{{2, 0, 1, 2}},
	{{2, 0, 2, 0}},
	{{2, 0, 2, 3}},
	{{2, 0, 2, 1}},
	{{2, 0, 2, 2}},
	{{2, 3, 0, 0}},
	{{2, 3, 0, 3}},
	{{2, 3, 0, 1}},
	{{2, 3, 0, 2}},
	{{2, 3, 3, 0}},
	{{2, 3, 3, 3}},
	{{2, 3, 3, 1}},
	{{2, 3, 3, 2}},
	{{2, 3, 1, 0}},
	{{2, 3, 1, 3}},
	{{2, 3, 1, 1}},
	{{2, 3, 1, 2}},
	{{2, 3, 2, 0}},
	{{2, 3, 2, 3}},
	{{2, 3, 2, 1}},
	{{2, 3, 2, 2}},
	{{2, 1, 0, 0}},
	{{2, 1, 0, 3}},
	{{2, 1, 0, 1}},
	{{2, 1, 0, 2}},
	{{2, 1, 3, 0}},
	{{2, 1, 3, 3}},
	{{2, 1, 3, 1}},
	{{2, 1, 3, 2}},
	{{2, 1, 1, 0}},
	{{2, 1, 1, 3}},
	{{2, 1, 1, 1}},
	{{2, 1, 1, 2}},
	{{2, 1, 2, 0}},
	{{2, 1, 2, 3}},
	{{2, 1, 2, 1}},
	{{2, 1, 2, 2}},
	{{2, 2, 0, 0}},
	{{2, 2, 0, 3}},
	{{2, 2, 0, 1}},
	{{2, 2, 0, 2}},
	{{2, 2, 3, 0}},
	{{2, 2, 3, 3}},
	{{2, 2, 3, 1}},
	{{2, 2, 3, 2}},
	{{2, 2, 1, 0}},
	{{2, 2, 1, 3}},
	{{2, 2, 1, 1}},
	{{2, 2, 1, 2}},
	{{2, 2, 2, 0}},
	{{2, 2, 2, 3}},
	{{2, 2, 2, 1}},
	{{2, 2, 2, 2}},
};
